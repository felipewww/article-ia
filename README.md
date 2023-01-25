buscar todos os artigos que eu não vi dos meus grupos

buscar todos os usuários do mesmo grupo que LERAM ARTIGOS QUE EU NÃO LI

preciso saber qual o ARTIGO mais proximo do usuario, artigos tem qtde de views, tags

faz a priemira CARGA FULL, calculando todos as recomendações, assim que o user chegar no "final" das recomendações, carrega só pra ele novamente, assim o script fica mais leve

R1 - ja vai filtrar isso na consulta inicial
R2 - ao invés de mais buscado pelo time, pode ser mais visto nos ultimos X dias, pega essa info da helpview
R3 - [inviável por enquanto] precisa de API para armazenar as consulta deste usuario, melhor deixar pra uma fase 2
R4 - minhas tags pode vir dos PINS ou dos lidos nos ultimos 2 dias - tag1, tag2, tag3, tag4, tag5


views_last_days = qtde de views nos ultimso 2 dias pelo time todo
tags_related - qtde de tags relacionadas as tags que eu ja li (talvez este indicador não faça tanto sentido)
last_update - ultimo update em dias, quanto menor, melhor

#dependencias

sudo apt-get install python3-pandas

sudo apt-get install python3-mysql.connector

https://cloud.google.com/sql/docs/mysql/connect-functions
#user o secret manager para env vars 

gcloud functions deploy sponsored-article-fn --region us-east4 --entry-point calc_sponsored --runtime python39 --trigger-topic sponsored-partial-topic 