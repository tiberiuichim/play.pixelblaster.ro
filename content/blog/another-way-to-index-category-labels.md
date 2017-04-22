+++
Tags = ["numpy","cookbook", "python", "MachineLearning", "keras"]
Description = "A silly way to use numpy and Tokenizer to replace words in a list with their index"
date = "2017-01-21T00:19:31+01:00"
title = "Another way to index category labels in categorization tasks"

+++

One common task in machine-based categorization tasks is to relabel data with
a numeric value, an index, where before that data was labeled with a string.

The basic Python code would be something like this:

```python
label_index = {}
labels = []
for l in string_labels:
    if l not in label_index:
        label_index[l] = len(label_index)
    labels.append(label_index[l])>
```

While writing that bit of code from above, I realized that a word tokenizer can
do the same thing. This would be the equivalent, using
`keras.preprocessing.text.Tokenizer` and numpy.

```python
t = Tokenizer()
t.fit_on_texts(_labels)
seqs = t.texts_to_sequences(_labels)
# seqs is a list of lists, something like:
# [[1], [2], [1], [3] ... ]
labels = np.array(seqs)[:,0] - 1
```

And now `t.word_index` holds the word to index mapping. `np.array(seqs)[:,0]`
returns a list with the first element (at index 0) of the second dimension of
the np array. The arithmetic operation of the end applies to each member of
the array and is needed because the tokenizer starts indexing words at 1.

Of course, the second way is convoluted, needs to process the list of labels
twice, uses two addon libraries (but probably already present for the domain
of this task) and needs some basic knowledge of numpy to be readable by others.
YMMV. I wonder which method is faster, on a bigger chunk of data.
