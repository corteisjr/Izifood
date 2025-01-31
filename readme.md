# E-commerce IziFood

Este é um projeto de e-commerce desenvolvido para fins de estudo. Ele inclui funcionalidades básicas de um sistema de comércio eletrônico, como cadastro de produtos, carrinho de compras e finalização de pedidos.

## Como Executar

1. Clone o repositório:

    ```sh
    git clone https://github.com/seu-usuario/ecommerce.git
    ```

2. Navegue até o diretório do projeto:

    ```sh
    cd ecommerce
    ```

3. Crie um ambiente virtual:

    ```sh
    python -m venv venv
    ```

4. Ative o ambiente virtual:

    - No Windows:

        ```sh
        venv\Scripts\activate
        ```

    - No Unix ou MacOS:

        ```sh
        source venv/bin/activate
        ```

5. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

6. Inicie o servidor:

    ```sh
    python manage.py runserver
    ```

8. Adicione um arquivo .env 

   ```sh
    SECRET_KEY = '...'
    POSTGRES_DB = '...'
    POSTGRES_USER = '...'
    POSTGRES_PASSWORD = '...'
    DB_PORT: '...'
   ```

9. Dentro do ecommerce_project , crie um arquivo local_setting.py e adicione:
    ```sh
        from decouple import config
        
        SECRET_KEY = config('SECRET_KEY')

        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': 'localhost',
            'PORT': config('DB_PORT', default='5434')
            }
        }
    ``
10. Abra seu navegador e acesse `http://localhost:8000` para ver o projeto em execução.

## Como Contribuir

1. Faça um fork do projeto.
2. Crie uma nova branch para sua feature ou correção de bug:
    ```sh
    git checkout -b minha-feature
    ```
3. Faça suas alterações e commit:
    ```sh
    git commit -m "Adiciona minha nova feature"
    ```
4. Envie suas alterações para o repositório remoto:
    ```sh
    git push origin minha-feature
    ```
5. Abra um Pull Request para a branch `main` do repositório original.


![image](https://github.com/user-attachments/assets/157d33ab-15aa-4b07-bdf2-8e478c83aa6e)
![image](https://github.com/user-attachments/assets/89db6825-0df3-46fd-b4a2-024bb3003eb1)
![image](https://github.com/user-attachments/assets/a8b6436d-0ec1-4ab3-b399-5da1b245d7ac)
![image](https://github.com/user-attachments/assets/1b8bd444-f892-478d-8217-b807dede012f)
![image](https://github.com/user-attachments/assets/1d5a727f-d09b-4c3a-a029-23b096dbaace)




