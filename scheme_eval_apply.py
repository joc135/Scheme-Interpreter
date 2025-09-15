import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

def scheme_apply(procedure, args, env):
    """Apply a Scheme procedure to ARGS in the given ENV."""
    if isinstance(procedure, BuiltinProcedure):
        # Convert Scheme list (Pair) to a Python list
        py_args = []
        while args is not nil:
            py_args.append(args.first)
            args = args.rest
        try:
            if procedure.need_env:
                return procedure.py_func(*py_args, env)
            else:
                return procedure.py_func(*py_args)
        except TypeError as e:
            raise SchemeError("incorrect number of arguments") from e

    elif isinstance(procedure, LambdaProcedure):
        # create a new frame and evaluate the body
        new_env = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)

    elif isinstance(procedure, MuProcedure):
        # Dynamic scoping: use the *calling* environment
        new_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)

    else:
        raise SchemeError(f"unknown procedure type: {procedure}")


def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3 (done by michael)
        operator = scheme_eval(expr.first, env)
        validate_procedure(operator)

        #Making the schem_eval function take one argument and operate in the current environment
        def temp_scheme_eval(expr): 
          return scheme_eval(expr, env)

        args = expr.rest.map(temp_scheme_eval)
        return scheme_apply(operator, args, env)
        # END PROBLEM 3



def eval_all(expressions, env):
  """Evaluate each expression in the Scheme list EXPRESSIONS in
  Frame ENV (the current environment) and return the value of the last.
  
  >>> eval_all(read_line("(1)"), create_global_frame())
  1
  >>> eval_all(read_line("(1 2)"), create_global_frame())
  2
  >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
  1
  >>> x
  2
  >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
  2
  """
  # BEGIN PROBLEM 6 (done by glenn benedict)
  if expressions is nil:
      return None
  elif len(expressions) == 1:
      return scheme_eval(expressions.first, env)
  else:
      result = None
      while expressions is not nil:
          result = scheme_eval(expressions.first, env)
          expressions = expressions.rest
      return result
  # END PROBLEM 6



##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
