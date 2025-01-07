# Python CircleCI 2.0 configuration file
#
# Check https://circleci.com/docs/2.0/language-python/ for more details
#
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3
    working_directory: ~/repo

    steps:
      - checkout

      # Download and cache dependencies
      - restore_cache:
          keys:
          - v1-dependencies-{{ checksum "dev-requirements.txt" }}
          # fallback to using the latest cache if no exact match is found
          - v1-dependencies-

      - run:
          name: install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            python -m pip install --upgrade pip
            pip install -r dev-requirements.txt

      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum "dev-requirements.txt" }}
        
  test:
    docker:
      - image: circleci/python:3
    working_directory: ~/repo

    steps:
      - checkout

      - restore_cache:
          key: v1-dependencies-{{ checksum "dev-requirements.txt" }}
      - run:
          name: run tests
          command: |
            mkdir -p /tmp/test-reports
            mkdir -p /tmp/pytest
            python3 -m venv venv
            . venv/bin/activate
            python -m pip install --upgrade pip
            pip install -r dev-requirements.txt
            pytest -v --junitxml=/tmp/pytest/results.xml >> /tmp/test-reports/pytest.out
            
            

      - store_artifacts:
          path: /tmp/test-reports
          destination: test-reports
      - store_artifacts:
          path: /tmp/pytest
          destination: pytest
      - store_test_results:
          path: /tmp/pytest


  deploy:
    docker:
      - image: circleci/python:3
    working_directory: ~/repo

    steps:
      - checkout

      - restore_cache:
          key: v1-dependencies-{{ checksum "dev-requirements.txt" }}

      - run:
          name: verify git tag vs version
          command: |
            python3 -m venv venv
            . venv/bin/activate
            python -m pip install --upgrade pip
            python setup.py verify

      - run: 
          name: make a source distribution
          command: |
            . venv/bin/activate
            python setup.py sdist

      - run:
          name: upload to pypi
          command: |
            . venv/bin/activate
            twine upload dist/*

workflows:
  version: 2
  build_test_deploy:
    jobs:
      - build:
          filters:
            tags:
              only: /.*/
      - test:
          filters:
            tags:
              only: /.*/
      - deploy:
          context: PYPI
          requires:
            - build
          filters:
            tags:
              only: /[0-9]+(\.[0-9]+)*/
            branches:
              ignore: /.*/
