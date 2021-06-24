# cmusicbox

Requer SQLite.

Aplicativo em python para registrar em um banco de dados SQLite as músicas tocadas. Criado para ser utilizado com o aplicativo cmus, mas aceita qualquer um que forneça externamente as informações da música. São necessários os nomes do artista, da música e do álbum.

    Uso: cmusicbox.py -a 'artista' -l 'álbum' -t 'música'

O arquivo get_info é um script em bash para pegar as informações necessárias do cmus e fornecer ao programa. Como o cmus executa o script a cada mudança de status, escrevi de uma maneira que ele não registre a mesma música várias vezes caso fique pausando e retomando a execução. Caso a música seja parada por completa (stop) e tocada novamente, irá registrar outra vez. Para funcionar é só ir nas opções do cmus e colocar o caminho para ele em 'status_display_program'.

Não esqueça de antes alterar o caminho para o cmusicbox.py no script para onde você colocou o executável.

O banco de dados é criado em $HOME/.config/cmusicbox

Essa é minha primeira experiência com banco de dados.

## cmusicbox-print

Exibe as 10 músicas e artistas mais tocados. Requer [tabulate](https://pypi.org/project/tabulate/).

    Usage: cmusicbox-print.py -t 'table format'

Visite a documentação do [tabulate](https://pypi.org/project/tabulate/) para diferente formatos. O padrão é "pretty".

----

# cmusicbox

Reqires SQLite.

Grabs the information of the currently playing song and stores in a SQLite database. I wrote this to use with cmus, but it works with any application that can outputs the song info. It needs the artist name, the album and song titles.

    Usage: cmusicbox.py -a 'artist' -l 'album' -t 'music'

The get_info file is a bash script to grab the info from cmus and feed to the program. Cmus runs the script at every status change (play, pause, stop, song change), so wrote in a way for it to not register if the song actually playing is the same as the one before in case it needs to be paused and resumed so it won't register the song again. If it is stopped and played, it will be registered again. Just put the path to the script in 'status_display_program' on cmus.

Don't forget to edit the path to cmusicbox.py to where you put the program.

The database will be criated in $HOME/.config/cmusicbox

## cmusicbox-print

Prints out the top 10 tracks and artists. Requires [tabulate](https://pypi.org/project/tabulate/).

    Usage: cmusicbox-print.py -t 'table format'

Check out [tabulate](https://pypi.org/project/tabulate/) documentation for different formats. The default is "pretty".
