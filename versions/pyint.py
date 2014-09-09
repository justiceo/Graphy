def main(args):
    eqn = math(args["eqn"])
    return { "integral": str(integrate(eqn)) }