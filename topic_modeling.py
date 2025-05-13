from gensim import corpora, models
import pyLDAvis.gensim_models
import pyLDAvis

def build_lda_model(token_lists, num_topics=5, passes=10):
    dictionary = corpora.Dictionary(token_lists)
    corpus = [dictionary.doc2bow(text) for text in token_lists]
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary,
                                num_topics=num_topics, passes=passes,
                                random_state=42)
    return lda_model, corpus, dictionary

def show_topics(lda_model, num_words=10):
    topics = lda_model.print_topics(num_words=num_words)
    for topic in topics:
        print(topic)

def visualize_lda(lda_model, corpus, dictionary):
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, 'lda_vietnamese.html')