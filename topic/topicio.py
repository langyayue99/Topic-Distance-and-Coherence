import os
from shutil import rmtree
from exceptions import Exception
from topic import Topic
import numpy as np

class TopicMissing(Exception):
    """
    topic Missing Exception
    """
    def __init__(self, message=""):
        print "One or several topics are missing "
        print message


class TopicIO:

    def write_topics(self, model, orig_dir, num_topics=10, num_words=10, output_dir="topic_list", split_sign=":"):
        """
        Write topics formulated by lda model for a corpus to files
        :param model: lda model
        :param num_topics: number of topics
        :param num_words: number of words
        :param output_dir: the name of the output directory
        """
        # if the output directory exist, delete it.
        # create a new empty output directory
        if os.path.exists(output_dir):
            rmtree(output_dir)

        os.makedirs(output_dir)

        # Get all topics
        topic_list = model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

        # Write each topic into a file with each line contains a word distribution value pair
        for index, topic in enumerate(topic_list):

            filename = output_dir + "/" + orig_dir + "_" + str(num_topics) + "_topic" + str(index) + ".txt"
            output_file = open(filename, "w")

            sorted_dist = list(sorted(topic[1]))

            for word_dist in sorted_dist:
                output = word_dist[0] + split_sign + str(word_dist[1])+"\n"
                output_file.write(output)

    def write_topics_from_tlist(self, tlist, output_dir, split_sign=":"):
        """
        Write topics from a list of topics
        :param tlist:a list of topics
        :param output_dir:output directory
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for index, topic in enumerate(tlist):
            ofile = open(output_dir + "/Topic"+str(index)+".txt","w")
            topic.sort()
            for wtuple in topic.list():
                wtuple = [str(w) for w in wtuple]

                oline = split_sign.join(wtuple)+"\n"
                ofile.write(oline)

                oline = ":".join(wtuple)+"\n"
                ofile.write(oline)


    def read_topics(self, input_dir="topic_list"):
        """
        Read all topics for a corpus from a directory named <input_directory>
        :param input_dir: the name of the input directory
        :return: a list of topics. Each topic is represented by a tuple which contains the topic id and its word distribution
        """
        topics = []
        for index, fname in enumerate(os.listdir(input_dir)):
            fname = input_dir + "/" + fname
            topic_i = self.read_topic(fname)
            topics.append(topic_i)
        return topics

    def read_topic(self, input_file="topic_list/topic_0.txt", split_sign=":"):
        """
        Read in a specific topic from a file named <input_file>
        :param input_file: the name of the file that stores the topic
        :return: a topic containing a list of word distribution tuples
        """
        # read in all ines of input except the last line which is an empty new line
        input_file = open(input_file, 'r')
        word_dist = input_file.readlines()

        # Create the topic object
        # The topic object contains a list of word distribution tuples
        topic = Topic()
        for dist in word_dist:
            dict = dist.strip().split(split_sign)
            topic.add((dict[0], float(dict[1])))

        return topic
