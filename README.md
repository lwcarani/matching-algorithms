# matching-algorithms
Implementation of the Gale-Shapley (also known as deferred acceptance) and Top Trading Cycle (TTC) algorithms for 2-sided matching.

The goal of the top trading cycles algorithm is to make trades amongst two sides of a market to find better allocations, i.e., ones where employees get jobs that they like better. More formally, we want to find a _stable allocation_, which means there is no trading coalition, which simply means there is no group of people that can swap amongst themselves so that every employee receives a job that they like better.

Another way to think about this algorithm is that employees are trading priorities with each other. Consider the below image, where `e1` is employee 1, `j1` is job 1, etc. We have the following preference lists:

`e1: [j2, j1]`<br>
`e2: [j1, j2]`<br>
`j1: [e1, e2]`<br>
`j2: [e2, e1]`

`e1`'s top choice is `j2`, and `e2`'s top choice is `j1`. However, `j1`'s "preference" is `e1`, and `j2`'s "preference" is `e2` (in this context, maybe employee 1 is the most qualified candidate for job 1. With students and schools in the school matching context, we might say that student 1 has the highest priority for school 1). In this example, since `e1, e2, j1, j2` form a cycle, the TTC algorithm would place employee 1 in job 2 `(e1, j2)` and employee 2 in job 1 `(e2, j1)`. We can see how in this example, even though `e1` and `e2` had higher priorities for `j1` and `j2`, respectively, by "trading their priorities," both employees were able to be placed in a job that they preferred more.


![image](https://github.com/lwcarani/matching-algorithms/assets/83194857/15bf2a3b-c493-4be8-b0e3-24df571b18bc)

(image created using https://madebyevan.com/fsm/)


Feedback and pull requests welcome!
