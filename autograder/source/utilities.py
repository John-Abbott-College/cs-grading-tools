import subprocess


def turtle_comment_out_mainloops(files):
    """Finds and replaces all instances of turtle.mainloop, turtle.done, turtle.exitonclick in the provided list of files."""
    cmd = ["sed"]
    args_mainloop = ["-i", "'s/turtle.mainloop()/#turtle.mainloop()/'"]
    args_done = ["-i", "'s/turtle.done()/#turtle.done()/'"]
    args_exitonclick = ["-i", "'s/turtle.exitonclick()/#turtle.exitonclick()/'"]

    for f in files:
        subprocess.run(cmd + args_mainloop + [f], check=True)
        subprocess.run(cmd + args_done + [f], check=True)
        subprocess.run(cmd + args_exitonclick + [f], check=True)
