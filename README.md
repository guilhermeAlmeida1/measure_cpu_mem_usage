Example usage:

```bash
$ python measure_cpu_mem_usage.py -c='./main options' -o=log.txt --time_step=50
Running process: ./main options
$ python parse.py log1.txt log2.txt -o outdir
$ ls outdir
'CPU usage (%).pdf'
'Memory usage (%).pdf'
'Memory usage (byte).pdf'
log1.pdf
log2.pdf
mem_active.pdf
```

[log1.pdf](https://github.com/user-attachments/files/16233138/log1.pdf)

[CPU usage (%).pdf](https://github.com/user-attachments/files/16233144/CPU.usage.pdf)

[Memory usage (%).pdf](https://github.com/user-attachments/files/16233146/Memory.usage.pdf)
