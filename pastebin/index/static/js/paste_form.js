$(document).ready(function() {
    var codeNode = document.querySelector('textarea');

    var codeEditor = CodeMirror.fromTextArea(codeNode, {
        lineNumbers: true
    });

    $('#id_syntax').on('change', function() {
        var getSyntax = function(name) {
            for(var i = 0; i < syntaxList.length; i += 1) {
                if(syntaxList[i].name == name) {
                    return syntaxList[i].id;
                }
            }

            console.warn('Mode not found: ' + name);

            return 'text';
        }

        codeEditor.setOption('mode', getSyntax($('option:selected', $(this)).text()));
    }).trigger('change');

    $('#id_users').select2();

    $('#id_visibility').on('change', function(e) {
        if($(this).val() == 'users') {
            $('label[for="id_users"]').show();
            $('#id_users').show();
            $('#id_users + .select2').show();
        } else {
            $('label[for="id_users"]').hide();
            $('#id_users').hide();
            $('#id_users + .select2').hide();
        }
    }).trigger('change');
});