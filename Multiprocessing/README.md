## Multiprocessing e Threading

Reaproveitamento de um código _WordCounter_ utilizando as lib Multiprocessing e explicitando diferenças da Threading.  
O "mp\_counter.py" seria a versão mais completa e útil do paralelismo para o mesmo fim. Ele distribui partes do arquivo que terá suas palavras contadas pelo número de processos em paralelo possíveis e mescla os resultados; ao final, compara o resultado com uma contagem de forma linear.  
  
~~~
\> python mp\_counter.py sherlock.txt output.txt
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
