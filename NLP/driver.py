
import csv
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import linear_model

train_path = "C:/Users/Clyde/Documents/visual studio 2015/Projects/Python/CourseraAI/NLP/aclImdb/train/" # use terminal to ls files under this directory
test_path = "C:/Users/Clyde/Documents/visual studio 2015/Projects/Python/CourseraAI/NLP/aclImdb/test/" # test data for grade evaluation
stpwrds_path = "C:/Users/Clyde/Documents/visual studio 2015/Projects/Python/CourseraAI/NLP/stopwords.en.txt"
output_path = "C:/Users/Clyde/Documents/visual studio 2015/Projects/Python/CourseraAI/NLP/"

def writefile(result, filename):
	with open(filename, 'w') as outputfile:
		for l in result:
			outputfile.write(l+'\n')

def imdb_tdata_preprocess(inpath, outpath=output_path, name="imdb_te.csv", mix=False):
	with open(outpath+name,'w', encoding="utf8",newline='\n') as csvfile:
		linenum = 1
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(["row_number","text"])
		posdir = inpath+"pos/"
		for filename in os.listdir(posdir):
			if filename.endswith(".txt"):
				f = open(posdir+filename,"r", encoding="utf8")
				l = f.readline()
				l = l.replace("\t"," ")
				l = l.replace("\n"," ")
				l = l.replace(",","")
				writer.writerow([linenum,l])
				linenum += 1
				f.close()
		negdir = inpath+"neg/"
		for filename in os.listdir(negdir):
			if filename.endswith(".txt"):
				f = open(negdir+filename,"r", encoding="utf8")
				l = f.readline()
				l = l.replace("\t"," ")
				l = l.replace("\n"," ")
				l = l.replace(",","")
				writer.writerow([linenum,l])
				linenum += 1
				f.close()

def imdb_data_preprocess(inpath, outpath=output_path, name="imdb_tr.csv", mix=False):
	with open(outpath+name,'w', encoding="utf8",newline='\n') as csvfile:
		linenum = 1
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(["row_number","text","polarity"])
		posdir = inpath+"pos/"
		for filename in os.listdir(posdir):
			if filename.endswith(".txt"):
				f = open(posdir+filename,"r", encoding="utf8")
				l = f.readline()
				l = l.replace("\t"," ")
				l = l.replace("\n"," ")
				l = l.replace(",","")
				writer.writerow([linenum,l,1])
				linenum += 1
				f.close()
		negdir = inpath+"neg/"
		for filename in os.listdir(negdir):
			if filename.endswith(".txt"):
				f = open(negdir+filename,"r", encoding="utf8")
				l = f.readline()
				l = l.replace("\t"," ")
				l = l.replace("\n"," ")
				l = l.replace(",","")
				writer.writerow([linenum,l,0])
				linenum += 1
				f.close()

if __name__ == "__main__":
	imdb_data_preprocess(inpath=train_path)

	stpwrds = open(stpwrds_path,"r",encoding="utf8")
	stopwords = []
	for word in stpwrds.readlines():
		stopwords.append(word.replace("\n",""))

	X=[]
	Y=[]
	with open(output_path+"imdb_tr.csv",'r',encoding="utf8") as file:
		rdr = csv.reader(file, delimiter=',')
		for row in rdr:
			X.append(row[1])
			Y.append(row[2])

	univectorizer = CountVectorizer(min_df=1, stop_words=stopwords, ngram_range=(1, 1))
	bivectorizer = CountVectorizer(min_df=1, stop_words=stopwords, ngram_range=(1, 2))
	unitfidfvec = TfidfVectorizer( stop_words=stopwords, ngram_range=(1, 1))
	bitfidfvec = TfidfVectorizer( stop_words=stopwords, ngram_range=(1, 2))

	unigram = univectorizer.fit_transform(X)
	bigram = bivectorizer.fit_transform(X)
	unitfidfgram = unitfidfvec.fit_transform(X)
	bitfidfgram = bitfidfvec.fit_transform(X)

	uvclf = linear_model.SGDClassifier(loss='hinge', penalty='l1')
	bvclf = linear_model.SGDClassifier(loss='hinge', penalty='l1')
	utvclf = linear_model.SGDClassifier(loss='hinge', penalty='l1')
	btvclf = linear_model.SGDClassifier(loss='hinge', penalty='l1')

	uvclf.fit(unigram, Y)
	bvclf.fit(bigram, Y)
	utvclf.fit(unitfidfgram, Y)
	btvclf.fit(bitfidfgram, Y)

	X=[]
	with open(output_path+"imdb_te.csv",'r', encoding='utf8') as file:
		rdr = csv.reader(file, delimiter=',')
		for row in rdr:
			X.append(row[1])

	univectorizer2 = CountVectorizer(min_df=1, stop_words=stopwords, ngram_range=(1, 1), vocabulary=univectorizer.get_feature_names())
	bivectorizer2 = CountVectorizer(min_df=1, stop_words=stopwords, ngram_range=(1, 2), vocabulary=bivectorizer.get_feature_names())
	unitfidfvec2 = TfidfVectorizer( stop_words=stopwords, ngram_range=(1, 1), vocabulary=unitfidfvec.get_feature_names())
	bitfidfvec2 = TfidfVectorizer( stop_words=stopwords, ngram_range=(1, 2), vocabulary=bitfidfvec.get_feature_names())

	unigram = univectorizer2.fit_transform(X)
	bigram = bivectorizer2.fit_transform(X)
	unitfidfgram = unitfidfvec2.fit_transform(X)
	bitfidfgram = bitfidfvec2.fit_transform(X)

	uvpred = uvclf.predict(unigram)
	bvpred = bvclf.predict(bigram)
	utvpred = utvclf.predict(unitfidfgram)
	btvpred = btvclf.predict(bitfidfgram)

	writefile(uvpred,output_path+'unigram.output.txt')
	writefile(bvpred,output_path+'bigram.output.txt')
	writefile(utvpred,output_path+'unigramtfidf.output.txt')
	writefile(btvpred,output_path+'bigramtfidf.output.txt')
