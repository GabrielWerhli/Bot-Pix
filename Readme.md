Instruções de Configuração e Uso

Token do Bot:

No trecho do código identificado como TOKEN, substitua "SEU TOKEN" pelo token fornecido pelo BotFather ao criar o seu bot no Telegram.​


Adição ao Grupo:

Adicione o bot ao grupo do Telegram onde os comprovantes de pagamento Pix serão compartilhados.​

Permissões:

Promova o bot a administrador do grupo e conceda-lhe as seguintes permissões:​

Excluir mensagens: Necessária para que o bot possa remover mensagens conforme configurado.

Outras permissões conforme necessário.

Envio dos Comprovantes:

Ao enviar um comprovante de pagamento Pix para o grupo, inclua na legenda da imagem o valor correspondente ao comprovante. O bot identificará e somará automaticamente os valores mencionados nas legendas.​

Comandos Disponíveis:

/start:

Inicia o bot no grupo e prepara-o para receber e processar os comprovantes enviados.

/total:

Exibe o total acumulado dos valores processados até o momento. Após 30 segundos, tanto o comando quanto a resposta serão automaticamente apagados pelo bot.

/limpar:

Remove as últimas 100 mensagens do grupo. Utilize este comando com cautela, pois ele apagará mensagens recentes que podem ser importantes.

Observações Importantes:

Limitações de Exclusão de Mensagens:

O Telegram permite que bots excluam apenas mensagens enviadas nos últimos dois dias (48 horas). Mensagens mais antigas não podem ser deletadas pelo bot.​

Mensagens Fixadas:

O comando /limpar pode não remover mensagens fixadas no grupo.​

Responsabilidade no Uso:

Utilize o comando /limpar com discernimento para evitar a remoção acidental de mensagens importantes.
