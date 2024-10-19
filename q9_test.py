#!/usr/bin/env python3

import nltk
import time
import multiprocessing

grammar = nltk.CFG.fromstring("""
    S -> NP VP | NP VP Con NP VP | NP VP Con VP | 'there' VP PP
    NP -> Det ADJP Noun | Det Noun | Noun Adj | Noun | Det Adj Noun PP | ADJP Noun | Adj Noun Part | Det Noun PP
    ADJP -> Adj ADJP | Adj
    VP -> Verb Adv PP | Verb NP | Verb PP | Verb Adj Adv | Mod Adv Verb Adv
    PP -> Prep NP
    Det -> 'the' | 'a' | 'his' | 'this'
    Con -> 'and' | 'but'
    Noun -> 'dog' | 'chair' | 'back' | 'somebody' | 'coffee' | 'we' | 'walk' | 'park' | 'vinny' | 'dogs' | 'it' | 'angels' | 'head' | 'pin'
    Adj -> 'cheerful' | 'black' | 'sleepy' | 'yellow' | 'downstairs' | 'three' | 'other' | 'long' | 'sunny' | '49'
    Mod -> 'might'
    Verb -> 'slept' | 'stretched' | 'made' | 'had' | 'played' | 'was' | 'be' | 'are'
    Part -> 'dancing'
    Prep -> 'by' | 'to' | 'with' | 'on' | 'of'
    Adv -> 'quietly' | 'today' | 'not' | 'tomorrow'
""")

rd_parser = nltk.RecursiveDescentParser(grammar)

sentences = [
    "The cheerful black dog slept quietly by the chair.",
    "A sleepy yellow dog stretched his back.",
    "Somebody downstairs made the coffee.",
    "We had a long walk to the park and Vinny played with three other dogs.",
    "It was sunny today but might not be tomorrow.",
    "There are 49 angels dancing on the head of this pin."
]

def get_parse_time(sent):
    runs = 1000
    start_time = time.time()
    for i in range(runs):
        better_sent = sent.lower().replace(".", "").split()
        trees_generator = rd_parser.parse(better_sent)
        trees = list(trees_generator)
        print(f"We are at {i}/{runs}", end="\r")
        #for tree in trees:
                #tree.pretty_print()
    end_time = time.time()
    total_time = end_time - start_time
    average_time = total_time/runs
    return average_time

def thread_helper(sent):
    passed_time = get_parse_time(sent)
    print(f"for sentence {sent} it took {passed_time}")


thread_array = []
with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
    results = pool.map(thread_helper, sentences)
