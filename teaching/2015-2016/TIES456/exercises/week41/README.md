
# Goal
The goal of the task is to get familiar with the Spring framework and use it for authentication.

# Prerequisites
Learn about spring boot (embedded application server for spring applications that automates a lot of spring application related configuration based on the libraries found in the classpath)
[https://spring.io/guides/gs/spring-boot/](https://spring.io/guides/gs/spring-boot/)
    
Learn how to use spring CRUD repositories (note, that these are available only in Spring 4) 
[https://spring.io/guides/gs/accessing-data-mongodb/](https://spring.io/guides/gs/accessing-data-mongodb/) explains how to set it up in the easiest possible way and
[http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/](http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/) contains more information on how to use it.

Check out some basic information about spring security from [http://www.mkyong.com/spring-security/spring-security-hello-world-annotation-example/](http://www.mkyong.com/spring-security/spring-security-hello-world-annotation-example/).
Your users will be stored in your mongodb database. MongoDB can be downloaded from [here](https://www.mongodb.org/downloads#production)
    
You can start the database by going to the `<installation directory>/bin/` directory and running `mongod.exe` on Window or `./mongod --dbpath=path/to/where/you/want/mongodata/` on Linux.

A start for the application can be found from [Kamil's repository](https://github.com/kamiljano/teaching/tree/master/teaching-spring).

# Task

In this exercise you will write a spring application that registers users and lets them log in. The user should first be presented with a registration form with the following input fields:

* Name
* email address
* password 
* repeat password

Once the fields are filled, the user presses the "register" button. That triggers an HTTP POST request to the backend.
The backend then checks in the database if the user with the following email address already exists, if it does, it should return an error message to the client.
The backend should also make sure that the passwords are the same and at least 6 characters long and if they are not, it should return an appropriate error.
Whatever the error, it should be dynamically presented to the user without reloading the page.
If no error occurs during the registration, the user should be persisted with the provided email and password.

Once the user is registered, it should be possible for him to log in. You should use spring security framework for that purpose.
When the user is finally logged in, just display his name.

#Hints

## Dependency injection in Spring
Spring framework provides you with dependency injection. In order to inject a resource into your controller or a service, you can use the @Autowired annotation, like in the following example

    @RestController
    public class IndexController {
        
        @Autowired
        private UserRepository userRepository;
    
        public void someMethodThatUsesUserRepository() {
            ...
        }
    }

This way spring will automatically initialize the userRepository before executing any of your methods.

In order to enable the connection to mongodb database, first add annotation to your configuration class/main class: @EnableMongoRepositories
and then add to your resources a file called application.properties and paste into it the following content

    spring.data.mongodb.host=localhost
    spring.data.mongodb.port=27017
    spring.data.mongodb.uri=mongodb://localhost/georpg
    spring.data.mongodb.repositories.enabled=true
    
If you decide to use gradle for your project, your build.gradle file could look as follows

    buildscript {
        ext {
            springBootVersion = '1.2.5.RELEASE'
        }
        repositories {
            mavenCentral()
            jcenter()
        }
        dependencies {
            classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
        }
    }
    
    group 'fi.teaching.spring'
    version '1.0-SNAPSHOT'
    
    apply plugin: 'java'
    apply plugin: 'idea'
    apply plugin: 'spring-boot'
    
    sourceCompatibility = 1.8
    targetCompatibility = 1.8
    
    repositories {
        mavenCentral()
    }
    
    dependencies {
        compile 'org.springframework.boot:spring-boot-starter-thymeleaf',
                'org.springframework.boot:spring-boot-starter-data-mongodb',
                'org.springframework.security:spring-security-web:4.0.1.RELEASE', //spring security
                'org.springframework.security:spring-security-config:4.0.1.RELEASE'
    
    }
