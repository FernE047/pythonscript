# Markov Chains

This folder contains 4 different implementations of Markov chain text generators. they are all very similar to each other, but with different implementations and different results. I wanted to see how different implementations would affect the results, and I also wanted to see how different parameters would affect the results.

## Projects

- [Markov by Letters](./markov_by_letters) : a Markov chain text generator that uses letters as states. it is the simplest implementation, but it produces the worst results.
- [Markov by Words](./markov_by_words/README.md) : Various implementations of a Markov chain text generator that uses words as states. they differ by how many previous states they use to predict the next state, by how many files they use to save the states and if they use ponctuation and spaces as states or not. totalizing 8 different implementations.
- [Markov by Messages](./markov_by_messages) : a Markov chain text generator that uses words as states, but it also uses the whatsapp message boundaries for outcomes. the first implementations used conversations I had with friends. I used to be very chatty.
- [Markov Fanfics](./markov_fanfics) : a Markov chain text generator that uses words as states, but it is trained on fanfics from [Spirit Fanfiction](https://www.spiritfanfiction.com/). it downloads 10k fanfics on various fandoms and uses them to train the Markov chain. this was before I learnt about licenses and stuff, so I didn't care about the legality of downloading and using those fanfics. I wouldn't do it now, but keeping it here to save the code.
