                    % rebase('base.tpl', titulo='Gestão de Clientes - Bottle + SQLite')
                    % for id_, nome, email, telefone in lista_clientes:
                <tr>
                    <td>{{id_}}</td>
                    <td>{{nome}}</td>
                    <td>{{email}}</td>
                    <td>{{telefone}}</td>                    
                    <td>
                        <a class="btn-edit" href="/editar/{{id_}}">Editar</a>
                        <a class="btn-del" href="/deletar/{{id_}}">Excluir</a>
                    </td>
                </tr>
                % end
