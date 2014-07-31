def main(args):
    eqn = math(args["eqn"])
    return { "solution": str(solve(eqn)) }