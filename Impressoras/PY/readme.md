Este script procura impressoras numa intranet e, baseado na tag <titulo>, verifica se elas estão online e no IP estabelecido à mesma. 

Basta inserir os dados de quantas impressoras quiser como objetos no array

O sript tem duas interfaces de output: terminal e arquivo log. Este último contém códigos de erro do módulo requests. O primeiro, apenas do print() para ficar mais "user friendly".