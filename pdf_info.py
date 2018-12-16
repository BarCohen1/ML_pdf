
# IMPORTS
import numpy as np
import zipfile
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
# import gensim
import get_pdf_data
import os
import pandas as pd
# from gensim.models import word2vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

class Lib:
    # Class holding information regarding the corpus
    trouble_shooting_sections_found = 0
    class Pdf: # small helper class - representing a pdf
        def __init__(self, name, content, trouble_shooting_sec):
            self.title = name # pdf title
            self.content = content # whole pdf content
            self.tf_idf = None # top 15 TF_IDF valued terms in pdf, excluding stop words0
            self.trouble_shooting_section = trouble_shooting_sec # troubleshooting section

    def __init__(self, calc_svd, calc_word_count, calc_word2vec):
        self.pdf_repository = os.fsencode("pdfs/batch4") # our working repository folder
        self.max_pdfs_num = np.inf
        self.content = []
        self.word2vec_model = None
        self.lib = self.get_pdf_tuples(calc_word2vec) # fill library with pdf objects according to repository
        self.vect_model = None
        self.word_counts_tf_idf = None # will hold tf_idf word_count vector after fit transform
        if calc_word_count: self._calc_word_count('english') # generate and save vectors excluding english stop words
        if calc_svd: self.svd_model = self._gen_SVD() # will hold svd model

    def __repr__(self):
        return str(self.lib)

    def print_only_enter_params(self, print_author, print_title, print_content):
        # helper print function, can print according to entered params
        for pdf in self.lib:
            ret = ''
            if print_author: ret += pdf.author
            if print_title: ret += pdf.title
            if print_content: ret += pdf.content
            if ret != '': print(ret)
        print('Over all pdf in lib: ', len(self.lib))

    def get_pdf_tuples(self, calc_word2vec):
        "main pdf object generator func, traverses over entere pdf_repository and extracts pdfs"
        def save_troubleshooting(index:int, filename , txt:""):
            file = open(str(index)+filename+".txt", "w", encoding="utf-8")
            file.write(txt)
            print("writing troubleshoot segment to pdf index: " +str(index)+ " done")

        pdf_rep = [] # list of PDFs holding the pdf author , name and content in each tuple.
        word2vec_content = []
        for index ,file in enumerate(os.listdir(self.pdf_repository)):
            filename = os.fsdecode(file)
            if filename.endswith('.pdf') and index < self.max_pdfs_num:
                try:
                    print("creating pdf_content for index: ", index)
                    #pdf_content, trouble_shooting = get_pdf_data.pdf_to_text(filename)
                    trouble_shooting = get_pdf_data.pdf_to_text(filename) 
                    if trouble_shooting:
                        print('trouble shooting found for: ' +filename)
                        # print(trouble_shooting)

                        Lib.trouble_shooting_sections_found+=1
                        save_troubleshooting(index, filename, trouble_shooting)
                        #self.content.append(pdf_content) # fill content list
                        #pdf_rep.append(Lib.Pdf(index,pdf_content, trouble_shooting)) # create new pdf
                        # if calc_word2vec: word2vec_content.append(gensim.utils.simple_preprocess(pdf_content))
                except:
                    continue

        # if calc_word2vec: # if word2vec param was entered
            # self.word2vec_model = gensim.models.Word2Vec(sentences=word2vec_content, size=300, window=7, min_count=2, workers=10) #builds vocabulary & train
        print('Number of pdf extracted ' +str(len(pdf_rep)) + ' out of '+ str(self.max_pdfs_num))
        print('Number of troubleshooting sections found:' + str(Lib.trouble_shooting_sections_found))
        self.max_pdfs_num = len(pdf_rep)
        print("finished creating pdf lib")
        return pdf_rep

    ################################################ TF_IDF terms generator and cvs creator ########################
    def turn_to_pdf(self):
        for index ,file in enumerate(os.listdir("/cs/labs/dshahaf/bar371/my-first-venv/pdf_parser/test")):
            filename = os.fsdecode(file)
            os.system("pdftotext -layout "+filename)





    def _calc_word_count(self, with_stop_words):

        self.pipeline = Pipeline([
            ('vect', CountVectorizer(stop_words=with_stop_words)),
            ('tfidf', TfidfTransformer()),
            ('norm', Normalizer(norm='l2')),
        ])
        self.word_counts_tf_idf = self.pipeline.fit_transform(self.content)
        self.vocab = np.array(self.pipeline.named_steps['vect'].get_feature_names())  # get list of words
        print("finished piping")


    def generate_term_values(self, pdf, book_index):
        order = (-self.word_counts_tf_idf[book_index]).toarray().argsort().flatten()[:15]
        pdf.tf_idf = self.vocab[order]


    def calc_tf_tfidf_for_all_lib(self):
        # this function generates the top tf_idf for all terms in each pdf
        for index, pdf in enumerate(self.lib): # for each pdf generate top terms
            print("creating top tf_idf for pdf: ", index)
            self.generate_term_values(pdf, index)
        print("finished creating tf_idfs for all pdfs")


    def generate_csvs(self):
        "this function generates TF_IDF cvs file from the lib pdfs "
        def gen_row(tf_idf, index):
            # helper function, generate row with author name, pdf title , and entered to 15 terms
            row = [index]
            # terms = [term[0] for term in tf_tuples]
            row.extend(tf_idf)
            return row

        def create_csv(matrix, name):
            # given a matrix with lists of author, pdf title and top 15 terms, create csv according to name param
            with open(name, 'w',  encoding="utf-8") as csvfile: # creating appropriate csv
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                for row in matrix: # write rows to csv
                    filewriter.writerow(row)
        print("creating cvs")
        tf_idf_csv = [] # our row holders
        for pdf in self.lib: # for each pdf, generate row using gen_row helper func
            tf_idf_csv.append(gen_row(pdf.tf_idf, pdf.title))
        create_csv(tf_idf_csv, 'tf_idf.csv')
        print("finished creating csv")


    ################################################## similarty, SVD, TNSE, word2Vec and others ######################
    def pdfs_by_phrase(self, model, word_counts, search_query):
        "using cosain_similarty on all pdfs words to search for similarteis to search query"
        phrases_matrix = model.transform([search_query])  # convert search string into a vector using trained model
        similarities = cosine_similarity(word_counts, phrases_matrix[0]).flatten()  # compute similarity of the search string to each pdf
        similarity_order = (-similarities).argsort().flatten()[:15]  # sort pdf by similarity to the term
        return similarity_order, similarities, search_query

    def _gen_SVD(self):
        # generates SVD model
        from sklearn.decomposition import TruncatedSVD
        svd_model = TruncatedSVD(n_components=self.max_pdfs_num)
        text_matrix_svd = svd_model.fit_transform(self.word_counts_tf_idf)

        print('SVD: Transforming word counts ({}x{}) to ({}x{}). Components: ({}x{})'.format(self.word_counts_tf_idf.shape[0],
                                                                                             self.word_counts_tf_idf.shape[1],
                                                                                             text_matrix_svd.shape[0],
                                                                                             text_matrix_svd.shape[1],
                                                                                             svd_model.components_.shape[
                                                                                 0],
                                                                                             svd_model.components_.shape[
                                                                                                 1]))

        # print('Explained variance: {}'.format(np.sum(svd_model.explained_variance_)))
        return svd_model

    def get_SVD_term_compare(self, str_term):
        term_vector_representation = self.svd_model.transform(self.pipeline.transform([str_term]))
        print('Term preresentation size: {}'.format(term_vector_representation.shape))
        similarities = cosine_similarity(term_vector_representation.reshape((1, self.max_pdfs_num)),
                                         self.svd_model.components_.T)  # find similarty between word and other docs
        print('Compared vector "{}" to {} other terms'.format(str_term, similarities.shape[1]))
        similarity_order = (-similarities).argsort().flatten()[:15]  # sort terms by similarity to the term

        for index, id in enumerate(similarity_order):
            print('{0:d}. {1:s} {2:2.2f}'.format(index, self.pipeline.named_steps['vect'].get_feature_names()[id],
                                                 similarities[0][id]))

    def word_2_vec_similarty(self):
        try:
            print(self.word2vec_model.wv.most_similar(positive=['phone', 'digital'], negative=['next'], topn=25))
        except:
            print('vec similarty failed')
            return

    def get_SVD_similarty_by_index(self, index):
        for word in self.lib[index].tf_idf:
            print("comparing " + word + "by SVD to repo")
            self.get_SVD_term_compare(word)

    def tsne_plot(self):
        "Creates and TSNE model and plots it"
        labels = []
        tokens = []

        for word in self.word2vec_model.wv.vocab:
            tokens.append(self.word2vec_model[word])
            labels.append(word)

        tsne_model = TSNE(perplexity=10, n_components=2, init='pca', n_iter=251, random_state=10)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])

        plt.figure(figsize=(16, 16))
        for i in range(len(x)):
            plt.scatter(x[i], y[i])
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        plt.show()


    def print_result(self, org_pharse,book_index_arry,similarty_arry):
        # print simlarty results for entered book_index_arr and similarty_arr
        matrix = []
        # generate similarty matrix
        for book_index, similarty in zip(book_index_arry, similarty_arry):
            matrix.append([libar.lib[book_index].author, libar.lib[book_index].title, similarty])

        #creates csv according to matrix, with name as the searched pharse
        with open(org_pharse, 'w', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            for row in matrix:
                filewriter.writerow(row)


def get_similary_for_pharses(pharses, libar):
    for phrase in pharses:
        book_index_arr , similarty_arr, s_pharse = libar.books_by_phrase(libar.pipeline , libar.word_counts_tf_idf
                                                   , phrase)
        libar.print_result(s_pharse, book_index_arr, similarty_arr)


######################################################################################################################


if __name__ == '__main__':

    # loading pdf to library
    libar = Lib(False, False, False)

    #generating tf_idf values and csvs
    # libar.calc_tf_tfidf_for_all_lib()
    # libar.generate_csvs()
    # libar.get_SVD_term_compare('phone')
    # libar.get_SVD_similarty_by_index(0)
    # libar.word_2_vec_similarty()
    # libar.tsne_plot()
    # simple search engine
    # libar.calc_word_count('english')
    # get_similary_for_pharses(
    #     ['in times of war and in times of peace', 'The boy always wanted to build a house on the beach'
    #         , 'Ever so slowly they began to understand love', 'A magic lamp suddenly appeared',
    #      'A horse, a sheep, a pig and a cow walk into a pub'], libar)


#
# pdftotext -layout NAME_OF_PDF.pd