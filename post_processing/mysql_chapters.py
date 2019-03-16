# coding=utf-8
import codecs
import re
import shutil

# TODO
# list blockquotes
# list tables

class MysqlChapters(object):
  def __init__(self, filepath):
    self.filepath = filepath
    self.backup_sql_file()
    self.broken_to_fixed = [(u'â€œ', u'“'),(u'â€™', u'’'),(u'â€˜', u'‘'),(u'â€”', u'–'),(u'â€“', u'—'),(u'â€¢', u'-'),
                            (u'â€¦', u'…'),(u'â‚¬', u'€'),(u'â€š', u'‚'),(u'â€¦', u'…'),(u'â€ž', u'„'),(u'â€˜', u'‘'),
                            (u'â€ ', u'†'),(u'â€¡', u'‡'),(u'â€°', u'‰'),(u'â€¹', u'‹'),(u'â€œ', u'“'),(u'â€™', u'’'),
                            (u'â€¢', u'•'),(u'â€“', u'–'),(u'â€”', u'—'),(u'â„¢', u'™'),(u'â€º', u'›'),(u'â€', u'”'),
                            (u'â€', u'”'),(u'Ã€', u'À'),(u'Ã‚', u'Â'),(u'Æ’', u'ƒ'),(u'Ãƒ', u'Ã'),(u'Ã„', u'Ä'),
                            (u'Ã…', u'Å'),(u'Ã†', u'Æ'),(u'Ã‡', u'Ç'),(u'Ë†', u'ˆ'),(u'Ãˆ', u'È'),(u'Ã‰', u'É'),
                            (u'Å ', u'Š'),(u'ÃŠ', u'Ê'),(u'Ã‹', u'Ë'),(u'Å’', u'Œ'),(u'ÃŒ', u'Ì'),(u'Å½', u'Ž'),
                            (u'ÃŽ', u'Î'),(u'Ã',  u'Ï'),(u'Ã',  u'Ð'),(u'Ã‘', u'Ñ'),(u'Ã’', u'Ò'),(u'Ã“', u'Ó'),
                            (u'Ã”', u'Ô'),(u'Ã•', u'Õ'),(u'Ã–', u'Ö'),(u'Ã—', u'×'),(u'Ëœ', u'˜'),(u'Ã˜', u'Ø'),
                            (u'Ã™', u'Ù'),(u'Å¡', u'š'),(u'Ãš', u'Ú'),(u'Ã›', u'Û'),(u'Å“', u'œ'),(u'Ãœ', u'Ü'),
                            (u'Å¾', u'ž'),(u'Ãž', u'Þ'),(u'Å¸', u'Ÿ'),(u'ÃŸ', u'ß'),(u'Â ', u' '),(u'Ã ', u'à'),
                            (u'Â¡', u'¡'),(u'Ã¡', u'á'),(u'Â¢', u'¢'),(u'Ã¢', u'â'),(u'Â£', u'£'),(u'Ã£', u'ã'),
                            (u'Â¤', u'¤'),(u'Ã¤', u'ä'),(u'Â¥', u'¥'),(u'Ã¥', u'å'),(u'Â¦', u'¦'),(u'Ã¦', u'æ'),
                            (u'Â§', u'§'),(u'Ã§', u'ç'),(u'Â¨', u'¨'),(u'Ã¨', u'è'),(u'Â©', u'©'),(u'Ã©', u'é'),
                            (u'Âª', u'ª'),(u'Ãª', u'ê'),(u'Â«', u'«'),(u'Ã«', u'ë'),(u'Â¬', u'¬'),(u'Ã¬', u'ì'),
                            (u'Â­', u'­'),(u'Ã­', u'í'),(u'Â®', u'®'),(u'Ã®', u'î'),(u'Â¯', u'¯'),(u'Ã¯', u'ï'),
                            (u'Â°', u'°'),(u'Ã°', u'ð'),(u'Â±', u'±'),(u'Ã±', u'ñ'),(u'Â²', u'²'),(u'Ã²', u'ò'),
                            (u'Â³', u'³'),(u'Ã³', u'ó'),(u'Â´', u'´'),(u'Ã´', u'ô'),(u'Âµ', u'µ'),(u'Ãµ', u'õ'),
                            (u'Â¶', u'¶'),(u'Ã¶', u'ö'),(u'Â·', u'·'),(u'Ã·', u'÷'),(u'Â¸', u'¸'),(u'Ã¸', u'ø'),
                            (u'Â¹', u'¹'),(u'Ã¹', u'ù'),(u'Âº', u'º'),(u'Ãº', u'ú'),(u'Â»', u'»'),(u'Ã»', u'û'),
                            (u'Â¼', u'¼'),(u'Ã¼', u'ü'),(u'Â½', u'½'),(u'Ã½', u'ý'),(u'Â¾', u'¾'),(u'Ã¾', u'þ'),
                            (u'Â¿', u'¿'),(u'Ã¿', u'ÿ'),(u'Ã', u'Ý'),(u'Ã', u'Á'),(u'Ã', u'Í')]


  def backup_sql_file(self):
    shutil.copy(self.filepath, "{0}.backup".format(self.filepath))


  def check_for_broken_unicode(self):
    text = codecs.open(self.filepath, 'r', encoding='utf-8').read()
    broken = False
    for (garble, c) in self.broken_to_fixed:
      if text.find(garble):
        broken = True
        break
    return broken


  def fix_unicode(self):
    text = codecs.open(self.filepath, 'r', encoding='utf-8').read()
    for (garble, correct) in self.broken_to_fixed:
      if text.find(garble) > -1:
        print u"replacing {0} -> {1}".format(garble, correct)
        text.replace(garble, correct)
    with codecs.open(self.filepath, 'w', encoding='utf-8') as f:
      f.write(text)


  def extract_images(self, outputfile):
    text = codecs.open(self.filepath, 'r', encoding='utf-8').read()
    regex = "([^\" ]+\\.(?:jpg|gif|png|jpeg|bmp))"
    imgs = set(re.findall(regex, text))
    print "Writing {0} image filenames to {1}".format(len(imgs), outputfile)
    with codecs.open(outputfile, 'w', encoding='utf-8') as f:
      f.write("\n".join(imgs))
      f.close()


  def extract_links(self, outputfile):
    text = codecs.open(self.filepath, 'r', encoding='utf-8').read()
    regex = "(\S+\/\S+)"
    links = set(re.findall(regex, text))
    print "Writing {0} links to {1}".format(len(links), outputfile)
    with codecs.open(outputfile, 'w', encoding='utf-8') as f:
      f.write("\n".join(links))
      f.close()


  def html_report(self, outputfile):
    text = codecs.open(self.filepath, 'r', encoding='utf-8').read()
    regex = "<(blockquote|table)"
    html_tags = set(re.findall(regex, text))
    html_tags_grouped = [[x, html_tags.count(x)] for x in set(html_tags)]
    print "Writing {0} filenames to {1}".format(len(html_tags_grouped), outputfile)
    with codecs.open(outputfile, 'w', encoding='utf-8') as f:
      f.write("\n".join(html_tags_grouped))
      f.close()