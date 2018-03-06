import csv
import codecs
import json
from lxml import etree, objectify
from tei_reader import TeiReader

class dict_update():

	def get_tag_with_ns(self, tag_name):
		return '{%s}%s' % (self.namespase, tag_name)

	def addElement(self, father, text_):
		form_ = objectify.Element(self.get_tag_with_ns('form'),nsmap = {None:self.namespase})
		orth_ = objectify.SubElement(form_, 'orth',nsmap = {None:self.namespase})
		orth_[0] = text_

		gramGrp_ = objectify.SubElement(form_, self.get_tag_with_ns('gramGrp'),nsmap = self.fullnamespase,)
		pos_ = objectify.SubElement(gramGrp_, self.get_tag_with_ns('pos'),nsmap = self.fullnamespase)
		pos_[0] = 'n'
		gen_ = objectify.SubElement(gramGrp_, self.get_tag_with_ns('gen'),nsmap = self.fullnamespase)
		gen_[0] = 'f'

		father.append(form_)

	def processBlock(self,block,down_level = False):
		childrens = block.getchildren()
		for children in childrens:
			if children.tag == self.get_tag_with_ns('form'):
				try:
					orth_ = children['orth']
					if orth_.text in self.infinitive_arr:
						otehr_words = self.other_dict[orth_.text]	
						for word in otehr_words:
							self.addElement(block,word)

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


	def processCSV(self,iterator):
		self.infinitive_arr.clear()
		self.other_dict.clear()
		for row in iterator:
			self.infinitive_arr.append(row[0].strip())
			self.other_dict.update({row[0]:[i.strip() for i in row[1:]]})

	def pars(self,delimiter=';'):
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
			sss = etree.tostring(tei_,encoding='UTF-8',pretty_print=True)
			f.write(sss)
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
