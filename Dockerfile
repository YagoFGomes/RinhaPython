# Usar a imagem base Python Alpine
FROM python:3.9-alpine

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho no container
COPY . /app

# Instalar o GCC e o musl-dev para compilar dependências
RUN apk add --no-cache gcc musl-dev

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 8000
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]