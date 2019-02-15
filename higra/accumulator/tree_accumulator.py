############################################################################
# Copyright ESIEE Paris (2018)                                             #
#                                                                          #
# Contributor(s) : Benjamin Perret                                         #
#                                                                          #
# Distributed under the terms of the CECILL-B License.                     #
#                                                                          #
# The full license is in the file LICENSE, distributed with this software. #
############################################################################

import higra as hg


@hg.argument_helper(hg.CptValuedHierarchy)
def accumulate_parallel(node_weights, accumulator, tree):
    """
    For each node i of the tree: accumulates values of the children of i in the node_weights array and put the result
    in output. i.e. output(i) = accumulate(node_weights(children(i)))

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    res = hg._accumulate_parallel(tree, node_weights, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(("tree", hg.CptHierarchy))
def accumulate_sequential(leaf_data, accumulator, tree, leaf_graph=None):
    """
    Performs a sequential accumulation of node values from the leaves to the root.
    For each leaf node i, output(i) = leaf_data(i).
    For each node i from the leaves (excluded) to the root, output(i) = accumulate(output(children(i)))

    :param leaf_data: array of weights on the leaves of the tree
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param leaf_graph: graph of the tree leaves (optional, deduced from :class:`~higra.CptHierarchy`)
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        leaf_data = hg.linearize_vertex_weights(leaf_data, leaf_graph)
    res = hg._accumulate_sequential(tree, leaf_data, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy)
def propagate_sequential(node_weights, condition, tree):
    """
    Conditionally propagates parent values to children.
    For each node i from the root to the leaves, if condition(i) then output(i) = output(tree.parent(i)) otherwise
    output(i) = input(i)

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param condition: Boolean array on the nodes of the tree
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    res = hg._propagate_sequential(tree, node_weights, condition)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy)
def propagate_sequential_and_accumulate(node_weights, accumulator, tree):
    """
    Propagates parent values to children anc accumulate with current value.
    For each node i from the root to the leaves, output(i) = accumulate(node_weights(i), output(parent(i))).

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    res = hg._propagate_sequential_and_accumulate(tree, node_weights, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy)
def propagate_parallel(node_weights, tree, condition=None):
    """
    The conditional parallel propagator defines the new value of a node as its parent value if the condition is true
    and keeps its value otherwise. This process is done in parallel on the whole tree. The default condition
    (if the user does not provide one) is true for all nodes: each node takes the value of its parent.

    The conditional parallel propagator pseudo-code could be::

        # input: a tree t
        # input: an attribute att on the nodes of t
        # input: a condition cond on the nodes of t

        output = copy(input)

        for each node n of t:
            if(cond(n)):
                output[n] = input[t.parent(n)]

            return output

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param condition: Boolean array on the nodes of the tree
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """

    if condition is not None:
        res = hg._propagate_parallel(tree, node_weights, condition)
    else:
        res = hg._propagate_parallel(tree, node_weights)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy, ("tree", hg.CptHierarchy))
def accumulate_and_add_sequential(node_weights, leaf_data, accumulator, tree, leaf_graph=None):
    """
    Performs a sequential accumulation of node values from the leaves to the root and
    add the result with the input array.

    For each leaf node i, output(i) = leaf_data(i).
    For each node i from the leaves (excluded) to the root, output(i) = input(i) + accumulate(output(children(i)))

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param leaf_data: Weights on the leaves of the tree
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param leaf_graph: graph of the tree leaves (optional (optional, deduced from :class:`~higra.CptValuedHierarchy`))
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        leaf_data = hg.linearize_vertex_weights(leaf_data, leaf_graph)
    res = hg._accumulate_and_add_sequential(tree, node_weights, leaf_data, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy, ("tree", hg.CptHierarchy))
def accumulate_and_multiply_sequential(node_weights, leaf_data, accumulator, tree, leaf_graph=None):
    """
    Performs a sequential accumulation of node values from the leaves to the root and
    add the result with the input array.

    For each leaf node i, output(i) = leaf_data(i).
    For each node i from the leaves (excluded) to the root, output(i) = input(i) + accumulate(output(children(i)))

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param leaf_data: Weights on the leaves of the tree
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param leaf_graph: graph of the tree leaves (optional (optional, deduced from :class:`~higra.CptValuedHierarchy`))
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        leaf_data = hg.linearize_vertex_weights(leaf_data, leaf_graph)
    res = hg._accumulate_and_multiply_sequential(tree, node_weights, leaf_data, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy, ("tree", hg.CptHierarchy))
def accumulate_and_min_sequential(node_weights, leaf_data, accumulator, tree, leaf_graph=None):
    """
    Performs a sequential accumulation of node values from the leaves to the root and
    add the result with the input array.

    For each leaf node i, output(i) = leaf_data(i).
    For each node i from the leaves (excluded) to the root, output(i) = input(i) + accumulate(output(children(i)))

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param leaf_data: Weights on the leaves of the tree
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param leaf_graph: graph of the tree leaves (optional (optional, deduced from :class:`~higra.CptValuedHierarchy`))
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        leaf_data = hg.linearize_vertex_weights(leaf_data, leaf_graph)
    res = hg._accumulate_and_min_sequential(tree, node_weights, leaf_data, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res


@hg.argument_helper(hg.CptValuedHierarchy, ("tree", hg.CptHierarchy))
def accumulate_and_max_sequential(node_weights, leaf_data, accumulator, tree, leaf_graph=None):
    """
    Performs a sequential accumulation of node values from the leaves to the root and
    add the result with the input array.

    For each leaf node i, output(i) = leaf_data(i).
    For each node i from the leaves (excluded) to the root, output(i) = input(i) + accumulate(output(children(i)))

    :param node_weights: Weights on the nodes of the tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param leaf_data: Weights on the leaves of the tree
    :param accumulator: see :class:`~higra.Accumulators`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param leaf_graph: graph of the tree leaves (optional (optional, deduced from :class:`~higra.CptValuedHierarchy`))
    :return: returns new tree node weights (Concept :class:`~higra.CptValuedHierarchy`)
    """
    if leaf_graph is not None:
        leaf_data = hg.linearize_vertex_weights(leaf_data, leaf_graph)
    res = hg._accumulate_and_max_sequential(tree, node_weights, leaf_data, accumulator)
    hg.CptValuedHierarchy.link(res, tree)
    return res
