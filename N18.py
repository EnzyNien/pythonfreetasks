import csv
import json
from lxml import etree, objectify

class dict_update():

	def clearData(self,result_data):
		repls = [b' xmlns:py="http://codespeak.net/lxml/objectify/pytype"', b' py:pytype="TREE"',b' py:pytype="str"']
		for repl in repls:
			result_data = result_data.replace(repl,b'')
		return result_data

	def get_tag_with_ns(self, tag_name):
		return '{%s}%s' % (self.namespase, tag_name)

	def addElement(self, father, other_words):
		attrib = {'type':'inflected'}
		form_ = objectify.Element(self.get_tag_with_ns('form'),nsmap = self.fullnamespase, attrib=attrib)
		form_.nsmap.pop('py')
		for idx, word in enumerate(other_words):
			orth_ = objectify.SubElement(form_, 'orth',nsmap = self.fullnamespase)
			orth_[idx] = word
		father.append(form_)

	def processBlock(self,block,down_level = False):
		childrens = block.getchildren()
		for children in childrens:
			added = False
			if children.tag == self.get_tag_with_ns('form'):
				try:
					orth_ = children['orth']
					if orth_.text in self.infinitive_arr:
						added = True
						other_words = self.other_dict[orth_.text]	
						self.addElement(block,other_words)
					else:
						added = False

				except AttributeError:
					if not down_level:
						self.error_log.append([{'typeError':'WORNING', 'line':str(children.sourceline), 'massage':'Block has not attr - orth. Will be searched in child elements'}])		
						self.processBlock(children,True)
					else:
						self.error_log.append([{'typeError':'ERROR', 'line':str(children.sourceline), 'massage':'Block has not attr - orth'}])	
						return
				else:
					if down_level:
						self.error_log.append([{'typeError':'FOUND', 'line':str(children.sourceline), 'massage':'Attr - orth found in child element'}])	
					elif added and not down_level:
						info = 'Attr - orth found. New elemens new items added: {}'.format(", ".join(other_words))
						self.error_log.append([{'typeError':'ALL OK', 'line':str(children.sourceline), 'massage':info}])


	def processCSV(self,iterator):
		self.infinitive_arr.clear()
		self.other_dict.clear()
		for row in iterator:
			self.infinitive_arr.append(row[0].strip())
			self.other_dict.update({row[0]:[i.strip() for i in row[1:]]})

	def pars(self,delimiter=';',clear_data=True):
		if not self.csv_name:
			err = 'csv_name file name error' 
			raise ValueError(err)
			return
		if not self.tei_name:
			err = 'tei_name file name error' 
			raise ValueError(err)
			return

		with open(self.csv_name,'r') as csvfile:
			iterator = csv.reader(csvfile, delimiter=delimiter)
			self.processCSV(iterator)

		with open(self.tei_name,'r',encoding="utf-8") as tiefile:
			xml = tiefile.read()

		tei_ = objectify.XML(xml)
		self.namespase = tei_.nsmap[None]
		self.fullnamespase = tei_.nsmap
		entry_ = tei_['text']['body']['entry']
		for block in entry_:
			self.processBlock(block)
		with open('result.tei', 'wb') as f:
			result_data = etree.tostring(tei_,encoding='UTF-8',pretty_print=True)
			if clear_data:
				result_data = self.clearData(result_data)
			f.write(result_data)
		with open('eror_log.txt', 'w') as f:
			json.dump(self.error_log,f)

	def __init__(self, csv_name = '', tei_name = ''):
		self.csv_name = str(csv_name)
		self.tei_name = str(tei_name)
		self.infinitive_arr = []
		self.other_dict = {}
		self.error_log = []


if __name__ == '__main__':
	dict_update('verbs.csv','spa-deu.tei').pars()
