$(document).ready(function() {
    
    // Приветствие
    alert('Добро пожаловать в ХерьAI!');
    
    // рега пользователя
    $('#registerForm').on('submit', function(e)
    {
        //получение важных переменных для кратких проверок
        var name = $('#name').val();
        var login = $('#login').val();
        var password = $('#password').val();
        var confirm = $('#confirm_password').val();
        if (name.trim() != name)
        {
            alert('Имя не должно начинаться или заканчиваться пробелами');
            return false;
        }
        
        if (login.trim() != login)
        {
            alert('Логин не должен начинаться или заканчиваться пробелами');
            return false;
        }
        
        if (password.trim() != password)
        {
            alert('Пароль не должен начинаться или заканчиваться пробелами');
            return false;
        }
        
        // Проверка на пустые поля
        if (name == '')
        {
            alert('Введите имя');
            return false;
        }
        
        if (login == '')
        {
            alert('Введите логин');
            return false;
        }

        if (password == '')
        {
            alert('Введите пароль');
            return false;
        }
        
        if (confirm == '')
        {
            alert('Подтвердите пароль');
            return false;
        }
        
        // Проверка длины
        if (login.length < 3)
        {
            alert('Логин должен быть минимум 3 символа');
            return false;
        }
        
        if (password.length < 6)
        {
            alert('Пароль должен быть минимум 6 символов');
            return false;
        }
        
        // Проверка совпадения паролей
        if (password != confirm) {
            alert('Пароли не совпадают');
            return false;
        }
        
        // Если всё ок, меняем кнопку
        $('#submitBtn').text('Регистрация...');
        $('#submitBtn').prop('disabled', true);
    });
    
    // ===== ВХОД =====
    $('#loginForm').on('submit', function(e) {
        var login = $('#login').val();
        var password = $('#password').val();
        
        // Проверка на пробелы
        if (login.trim() != login) {
            alert('Логин не должен начинаться или заканчиваться пробелами');
            return false;
        }
        
        if (password.trim() != password) {
            alert('Пароль не должен начинаться или заканчиваться пробелами');
            return false;
        }
        
        // Проверка на пустые поля
        if (login == '') {
            alert('Введите логин');
            return false;
        }
        
        if (password == '') {
            alert('Введите пароль');
            return false;
        }
        
        // Меняем кнопку
        $('#submitBtn').text('Вход...');
        $('#submitBtn').prop('disabled', true);
    });
    
    // картиночка хехехе
    var keys = [];
    
    $(document).on('keydown', function(e) {
        var key = e.key.toUpperCase();
        keys.push(key);
        
        if (keys.length > 3) {
            keys.shift();
        }
        
        if (keys[0] == 'Q' && keys[1] == 'W' && keys[2] == 'E') {
            // Открываем картинку
            var win = window.open('', '_blank');
            win.document.write('<html><head><title>Секрет</title></head><body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;"><img src="/static/i.png" style="max-width:100%; max-height:100%;"></body></html>');
            keys = [];
        }
    });
    
    // Анимация для кнопок
    $('button').hover(
        function() {
            $(this).css('transform', 'scale(1.05)');
        },
        function() {
            $(this).css('transform', 'scale(1)');
        }
    );
    $('.register-card, .login-card').fadeIn(500);
});