## Multiprocessing e Threading

Reaproveitamento de um código _WordCounter_ utilizando as lib Multiprocessing e explicitando diferenças da Threading.  
O "mp\_counter.py" seria a versão mais completa e útil do paralelismo para o mesmo fim. Ele distribui partes do arquivo que terá suas palavras contadas pelo número de processos em paralelo possíveis e mescla os resultados; ao final, compara o resultado com uma contagem de forma linear.  
  
~~~
> python mp_counter.py sherlock.txt output.txt
~~~
Output:
~~~Python
Multiprocessing took 4.69s
Starting "linear"
Equal? True
Linear took 18.33s
~~~
...Em um i3 7ªgen dual core, 4 threads  
Testado _for i in range(2,17,2)_.
  
Já o "shmem\_counter.py" foi uma tentativa de melhorar a performance usando o mesmo script, mas substituindo toda a serialização (uso das _queues_ e args de início dos processos) pelo uso de memória compartilhada. Teve uma performance muito abaixo do esperado além de levantar dúvida se o módulo _pickle_ está sendo usado (vai ser necessário alterar o código-fonte desse módulo para ter controle dos objetos serializados).

~~~
> python shmem_counter.py sherlock.txt output.txt
~~~
Output:
~~~Python
Strict parallel time took 10.52s
Multiprocessing took 11.07s
"pickle" in sys.modules = True
Starting "linear"
Equal? True
Linear took 18.33s
~~~

Por fim o "q_and_shmem_counter.py" faz uso tanto da serialização quanto da memória compartilhada, o que resultou em pequena melhora de desempenho.

~~~PowerShell
> hyperfine "py q_and_shmem_counter.py sherlock.txt output.txt"
Benchmark 1: py q_and_shmem_counter.py sherlock.txt output.txt
  Time (mean ± σ):      5.065 s ±  0.031 s    [User: 0.002 s, System: 0.015 s]
  Range (min … max):    5.025 s …  5.135 s    10 runs

> hyperfine "py mp_counter.py sherlock.txt output.txt"
Benchmark 1: py mp_counter.py sherlock.txt output.txt
  Time (mean ± σ):      5.120 s ±  0.043 s    [User: 0.005 s, System: 0.009 s]
  Range (min … max):    5.073 s …  5.198 s    10 runs
~~~
