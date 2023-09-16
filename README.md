# Final Project Template

Full Stack Project with Django, IBM CLOUDANT, Watson NLU and IBM CLOUD

The application is enable in :

´´´
https://vinijosenog-8000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/djangoapp/

´´´
You can run on your local machine using the commands bellow:

    - cd server/
    - pip install poetry
    - poetry install
    - poetry run python manage.py makemigrations
    - poetry run python manage.py migrate
    - poetry run python manage.py makemigrations djangoapp
    - poetry run python manage.py migrate djangoapp
    - poetry run python manage.py runserver

- Before running the application remember to duplicate the file ".env.sample" and set yours URL for each variable. You can use the values bellow for DEALERSHIP_URL and REVIEW_URL, but you still need a inscription for yout Watson NLP url and API_key
    - DEALERSHIP_URL=https://us-south.functions.appdomain.cloud/api/v1/web/d067e140-d663-4ff7-83fa-10f02c481aed/dealership-package/dealership
    - REVIEW_URL=https://us-south.functions.appdomain.cloud/api/v1/web/d067e140-d663-4ff7-83fa-10f02c481aed/dealership-package/review


- Commands to build in IBM CLOUD:

    - kubectl delete deployment dealership

    - ibmcloud cr image-rm us.icr.io/sn-labs-vinijosenog/dealership:latest && docker rmi us.icr.io/sn-labs-vinijosenog/dealership:latest

    - MY_NAMESPACE=$(ibmcloud cr namespaces | grep sn-labs-)
    - echo $MY_NAMESPACE

    - docker build -t us.icr.io/sn-labs-vinijosenog/dealership .

    - docker push us.icr.io/sn-labs-vinijosenog/dealership

    - kubectl apply -f deployment.yaml

    - kubectl port-forward deployment.apps/dealership 8000:8000

    - kubectl get pods
    
    - kubectl logs <pod name>   -c dealership

