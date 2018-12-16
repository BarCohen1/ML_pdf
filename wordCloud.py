from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import get_pdf_data
from os import path
from PIL import Image

def simple_cloud(pdf_name):
    pure_text = get_pdf_data.pdf_to_text(pdf_name +'.pdf')
    # pure_text ='\n'.join(pages)

    wordcloud = WordCloud(max_font_size=40)
    wordcloud = wordcloud.generate(pure_text)

    fig = plt.figure(figsize=(12,9))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    #fig.savefig(short_file_name + '.png', transparent=True, format='png')

def alise_cloud(pdf_name):
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    d = "C:\\Users\\Bar\\PycharmProjects\\pdf_parser"
    # Read the whole text.
    text = get_pdf_data.pdf_to_text(pdf_name +'.pdf')

    # read the mask / color image taken from
    # http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
    alice_coloring = np.array(Image.open(path.join(d, "alice.png")))
    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                   stopwords=stopwords, max_font_size=40, random_state=42)
    # generate word cloud
    wc.generate(text)

    # create coloring from image
    image_colors = ImageColorGenerator(alice_coloring)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    # recolor wordcloud and show
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
    plt.axis("off")
    plt.show()

alise_cloud('big')