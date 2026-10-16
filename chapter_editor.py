#!/usr/bin/env python3
# encoding: utf-8
import argparse
import re
import tkinter as tk
from tkinter import messagebox

import html
from html.parser import HTMLParser

import yaml
from pymysql import connect


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4"):
            self._parts.append("\n")

    def get_text(self):
        return html.unescape("".join(self._parts))


def strip_html(text):
    s = _HTMLStripper()
    s.feed(text or "")
    return s.get_text()


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def get_connection(cfg):
    return connect(
        host=cfg["db_host"],
        user=cfg["db_user"],
        password=cfg.get("db_password") or "",
        database=cfg["output_database"],
        charset="utf8mb4",
        use_unicode=True,
        autocommit=False,
    )


def fetch_chapter(conn, chapter_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM chapters WHERE id = %s", (chapter_id,))
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Chapter {chapter_id} not found in output database")
        return dict(zip(cols, row))


def db_update_chapter_text(cur, chapter_id, text):
    cur.execute("UPDATE chapters SET text = %s WHERE id = %s", (text, chapter_id))


def db_update_chapter_text_and_title(cur, chapter_id, text, title):
    cur.execute(
        "UPDATE chapters SET text = %s, title = %s WHERE id = %s",
        (text, title, chapter_id),
    )


def db_shift_later_chapters(cur, story_id, after_position):
    cur.execute(
        "UPDATE chapters SET position = position + 1 WHERE story_id = %s AND position > %s",
        (story_id, after_position),
    )


def db_insert_chapter(cur, story_id, position, title, author_id, text, date, notes, url):
    cur.execute(
        """INSERT INTO chapters (position, title, author_id, text, date, story_id, notes, url)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (position, title, author_id, text, date, story_id, notes, url),
    )


def db_trim_chapter(conn, chapter_id, trimmed_text):
    with conn.cursor() as cur:
        db_update_chapter_text(cur, chapter_id, trimmed_text)
    conn.commit()


def db_split_chapter(conn, chapter, before_text, after_text, title_part1, title_part2):
    story_id = chapter["story_id"]
    orig_position = chapter["position"]
    with conn.cursor() as cur:
        db_shift_later_chapters(cur, story_id, orig_position)
        db_update_chapter_text_and_title(cur, chapter["id"], before_text, title_part1)
        db_insert_chapter(
            cur,
            story_id=story_id,
            position=orig_position + 1,
            title=title_part2,
            author_id=chapter["author_id"],
            text=after_text,
            date=chapter["date"],
            notes=chapter["notes"],
            url=chapter["url"],
        )
    conn.commit()


class SplitChapterApp:
    def __init__(self, root, conn, chapter):
        self.root = root
        self.conn = conn
        self.chapter = chapter
        self.split_index = None

        root.title(f"Split Chapter: {chapter['title']}")

        info = tk.Frame(root)
        info.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            info,
            text=f"Chapter ID: {chapter['id']}  |  Story ID: {chapter['story_id']}  |  Position: {chapter['position']}",
        ).pack(side=tk.LEFT)

        text_frame = tk.Frame(root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            width=100,
            height=40,
            cursor="ibeam",
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)

        # Display stripped text; keep a mapping from display offset → raw HTML offset
        self._display_text, self._offset_map = self._build_display(chapter["text"] or "")
        self.text_widget.insert(tk.END, self._display_text)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.bind("<Button-1>", self.on_click)
        self.text_widget.bind("<ButtonRelease-1>", self.on_release)

        self.status_var = tk.StringVar(value="Click in the text to set a split point.")
        tk.Label(root, textvariable=self.status_var, fg="blue").pack(pady=4)

        counts_frame = tk.Frame(root)
        counts_frame.pack()
        self.before_var = tk.StringVar(value="Before: —")
        self.after_var = tk.StringVar(value="After: —")
        tk.Label(counts_frame, textvariable=self.before_var, width=30).pack(side=tk.LEFT, padx=10)
        tk.Label(counts_frame, textvariable=self.after_var, width=30).pack(side=tk.LEFT, padx=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.split_btn = tk.Button(
            btn_frame,
            text="Split at click point",
            state=tk.DISABLED,
            command=self.do_split,
            padx=20,
        )
        self.split_btn.pack(side=tk.LEFT, padx=10)
        self.trim_btn = tk.Button(
            btn_frame,
            text="Trim to selection",
            state=tk.DISABLED,
            command=self.do_trim,
            padx=20,
        )
        self.trim_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", command=root.quit, padx=20).pack(side=tk.LEFT, padx=10)

    def _build_display(self, raw_html):
        """
        Returns (display_text, offset_map) where offset_map[display_idx] = raw_idx.
        Strips HTML tags, converts block-level tags to newlines, unescapes entities.
        """
        display_chars = []
        offset_map = []  # display position i → raw HTML position
        raw = raw_html
        i = 0
        block_tags = {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4", "hr"}
        while i < len(raw):
            if raw[i] == "<":
                end = raw.find(">", i)
                if end == -1:
                    display_chars.append(raw[i])
                    offset_map.append(i)
                    i += 1
                    continue
                tag_content = raw[i + 1:end].strip().lower().lstrip("/").split()[0] if raw[i + 1:end].strip() else ""
                if tag_content in block_tags:
                    display_chars.append("\n")
                    offset_map.append(i)
                i = end + 1
            elif raw[i] == "&":
                end = raw.find(";", i)
                if end == -1 or end - i > 10:
                    display_chars.append(raw[i])
                    offset_map.append(i)
                    i += 1
                else:
                    entity = raw[i:end + 1]
                    decoded = html.unescape(entity)
                    for ch in decoded:
                        display_chars.append(ch)
                        offset_map.append(i)
                    i = end + 1
            else:
                display_chars.append(raw[i])
                offset_map.append(i)
                i += 1
        return "".join(display_chars), offset_map

    def on_click(self, event):
        idx = self.text_widget.index(f"@{event.x},{event.y}")
        display_offset = self._tk_index_to_char_offset(idx, self._display_text)
        # Map display offset back to raw HTML offset
        if display_offset < len(self._offset_map):
            raw_offset = self._offset_map[display_offset]
        else:
            raw_offset = len(self.chapter["text"] or "")
        self.split_index = raw_offset

        full_text = self.chapter["text"] or ""
        before_len = len(full_text[:raw_offset])
        after_len = len(full_text[raw_offset:])

        self.before_var.set(f"Before: {before_len:,} chars")
        self.after_var.set(f"After: {after_len:,} chars")
        self.status_var.set(f"Split point at raw HTML offset {raw_offset:,}. Click 'Split' to confirm.")
        self.split_btn.config(state=tk.NORMAL)

        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.tag_remove("split", "1.0", tk.END)
        self.text_widget.tag_add("split", idx)
        self.text_widget.tag_config("split", background="yellow")
        self.text_widget.config(state=tk.DISABLED)

    def _tk_index_to_char_offset(self, idx, text):
        line, col = map(int, idx.split("."))
        lines = text.split("\n")
        offset = sum(len(lines[i]) + 1 for i in range(line - 1))  # +1 for each \n
        return offset + col

    def on_release(self, event):
        try:
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            if sel_start != sel_end:
                self.trim_btn.config(state=tk.NORMAL)
                self.status_var.set("Text selected. Click 'Trim to selection' to keep only the selected text.")
                return
        except tk.TclError:
            pass
        self.trim_btn.config(state=tk.DISABLED)

    def do_trim(self):
        try:
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
        except tk.TclError:
            messagebox.showwarning("No selection", "Please select the text you want to keep.")
            return

        start_display = self._tk_index_to_char_offset(sel_start, self._display_text)
        end_display = self._tk_index_to_char_offset(sel_end, self._display_text)

        raw = self.chapter["text"] or ""
        raw_start = self._offset_map[start_display] if start_display < len(self._offset_map) else 0
        raw_end = self._offset_map[end_display] if end_display < len(self._offset_map) else len(raw)
        trimmed = raw[raw_start:raw_end]

        if not trimmed.strip():
            messagebox.showwarning("Empty selection", "The selected text is empty.")
            return

        if not messagebox.askyesno(
            "Confirm trim",
            f"This will replace the chapter text with the selected {len(trimmed):,} characters.\n\nThis cannot be undone. Continue?",
        ):
            return

        try:
            db_trim_chapter(self.conn, self.chapter["id"], trimmed)
            messagebox.showinfo("Done", f"Chapter {self.chapter['id']} trimmed to {len(trimmed):,} characters.")
            self.root.quit()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))

    def do_split(self):
        if self.split_index is None:
            return

        full_text = self.chapter["text"] or ""
        before_text = full_text[: self.split_index]
        after_text = full_text[self.split_index :]

        if not before_text.strip() or not after_text.strip():
            messagebox.showwarning("Invalid split", "Both parts must have content.")
            return

        base_title = re.sub(r"\s+Part \d+$", "", self.chapter["title"] or "").strip()
        title_part1 = f"{base_title} Part 1"
        title_part2 = f"{base_title} Part 2"

        try:
            db_split_chapter(self.conn, self.chapter, before_text, after_text, title_part1, title_part2)
            messagebox.showinfo(
                "Done",
                f"Chapter split successfully.\n\n"
                f"Chapter {self.chapter['id']} → '{title_part1}'\n"
                f"New chapter (position {self.chapter['position'] + 1}) → '{title_part2}'",
            )
            self.root.quit()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))


def main():
    import getpass

    parser = argparse.ArgumentParser(description="Split a chapter in the Open Doors output database")
    parser.add_argument("-p", "--properties_file", required=True, help="Path to yml config file")
    parser.add_argument("--chapter_id", required=True, type=int, help="ID of the chapter to split")
    args = parser.parse_args()

    cfg = load_config(args.properties_file)
    if not cfg.get("db_password"):
        cfg["db_password"] = getpass.getpass(f"MySQL password for {cfg['db_user']}@{cfg['db_host']}: ")
    conn = get_connection(cfg)
    chapter = fetch_chapter(conn, args.chapter_id)

    root = tk.Tk()
    root.geometry("1000x700")
    SplitChapterApp(root, conn, chapter)
    root.mainloop()
    conn.close()


if __name__ == "__main__":
    main()
