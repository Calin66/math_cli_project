import click
from logic import calc_pow, calc_fibonacci, calc_factorial
from models import PowRequest, FibRequest, FactRequest
from queue_handler import task_queue, start_worker

@click.group()
def cli():
    """Main CLI group."""
    pass

@cli.command()
@click.option('--base', type=int, required=True)
@click.option('--exp', type=int, required=True)
def power(base, exp):
    """Raise base to the power of exp."""
    request = PowRequest(base=base, exp=exp)
    task_queue.put(('power', request))
    print("[CLI] Task put in queue.", flush=True)
    task_queue.put(None)

@cli.command()
@click.option('--n', type=int, required=True)
def fibonacci(n):
    """Return the nth Fibonacci number."""
    request = FibRequest(n=n)
    task_queue.put(('fibonacci', request))
    print("[CLI] Task put in queue.", flush=True)
    task_queue.put(None)

@cli.command()
@click.option('--n', type=int, required=True)
def factorial(n):
    """Return the factorial of n."""
    request = FactRequest(n=n)
    task_queue.put(('factorial', request))
    print("[CLI] Task put in queue.", flush=True)
    task_queue.put(None)

if __name__ == '__main__':
    start_worker()
    cli()
    task_queue.join()
    wait_for_worker()

