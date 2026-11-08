# Day 10: token bill calculator
# Turns input and output tokens into a bill, for 1 ticket and for 1,000 tickets.
# Run: python bill_calculator.py
# With your own numbers from r.usage: python bill_calculator.py --input 200 --output 40
#
# Rates below: Gemini 3.8 Flash, paid tier, through 31 Dec 2026,
# from aistudio.google.com/docs/pricing (checked 8 Nov 2026).
# Rates change. Check the pricing page and update these two numbers yourself.

import argparse

INPUT_RATE_PER_1M = 0.75   # dollars per 1 million input tokens
OUTPUT_RATE_PER_1M = 3.75  # dollars per 1 million output tokens (includes thinking tokens)

TICKETS = 1000  # how many tickets for the "big bill" line


def bill(input_tokens, output_tokens):
    """Return (input cost, output cost, total) in dollars for one call."""
    input_cost = input_tokens * INPUT_RATE_PER_1M / 1_000_000
    output_cost = output_tokens * OUTPUT_RATE_PER_1M / 1_000_000
    return input_cost, output_cost, input_cost + output_cost


def money(dollars):
    """Show small dollar amounts without losing the digits."""
    if dollars < 0.01:
        return f"${dollars:.5f}"
    return f"${dollars:.2f}"


def print_bill(label, input_tokens, output_tokens):
    input_cost, output_cost, total = bill(input_tokens, output_tokens)
    print(label)
    print(f"  input  {input_tokens} tokens = {money(input_cost)}")
    print(f"  output {output_tokens} tokens = {money(output_cost)}")
    print(f"  1 ticket      = {money(total)}")
    print(f"  {TICKETS:,} tickets = {money(total * TICKETS)}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Token bill calculator")
    parser.add_argument("--input", type=int, default=200, help="input tokens (example: 200)")
    parser.add_argument("--output", type=int, default=40, help="output tokens (example: 40)")
    args = parser.parse_args()

    ratio = OUTPUT_RATE_PER_1M / INPUT_RATE_PER_1M
    print(f"Output is {ratio:g} guna mehenga than input at these rates.\n")

    print_bill("Your numbers (default = example numbers)", args.input, args.output)

    # The trap: same ticket, two ways of asking. Example numbers.
    print("The trap, with example numbers (same 200 input tokens):")
    print_bill('  "Detail mein samjhao" (ex. 800 output)', 200, 800)
    print_bill('  "1 line mein" (ex. 40 output)', 200, 40)

    print("Rule: jitna chahiye, utna maango.")


if __name__ == "__main__":
    main()
