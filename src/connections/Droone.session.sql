-- alter table Clientes_Droone rename tbl_clientes;
#  alterações de nome de atributos
# - tbl_circuitos 
alter table tbl_circuitos
    rename column IP_principal to ip_principal;
# - tbl_imagens
alter table tbl_imagens
    rename column ID_imagens to id_imagem;
alter table tbl_imagens
    rename column Timestamp_Criacao to timestamp_create;
alter table tbl_imagens
    rename column Full_Path to `path`;
alter table tbl_imagens
    rename column Data_Hora_Chegada to datetime_chegada;
alter table tbl_imagens
    rename column Data_Hora_Ultima_Mudanca to datetime_ultima_modificacao;
alter table tbl_imagens
    rename column Status_Imagem to `status`;