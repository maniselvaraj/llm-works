#python method to fetch all java files from github repo
import os
from langchain_community.document_loaders import GithubFileLoader

#
# [Document(metadata={'path': 'src/main/java/com/mani/llm/springboot/Application.java', 'sha': '47148df0f06714922a0b431e8f33c4d8e802c057',
#                     'source': 'https://api.github.com/maniselvaraj/springboot-demo/blob/main/src/main/java/com/mani/llm/springboot/Application.java'},
#           page_content='package com.mani.llm.springboot;\n\nimport java.util.Arrays;\n\nimport org.springframework.boot.CommandLineRunner;\nimport org.springframework.boot.SpringApplication;\nimport org.springframework.boot.autoconfigure.SpringBootApplication;\nimport org.springframework.context.ApplicationContext;\nimport org.springframework.context.annotation.Bean;\n\n@SpringBootApplication\npublic class Application {\n\n\tpublic static void main(String[] args) {\n\t\tSpringApplication.run(Application.class, args);\n\t}\n\n\t@Bean\n\tpublic CommandLineRunner commandLineRunner(ApplicationContext ctx) {\n\t\treturn args -> {\n\n\t\t\tSystem.out.println("Let\'s inspect the beans provided by Spring Boot:");\n\n\t\t\tString[] beanNames = ctx.getBeanDefinitionNames();\n\t\t\tArrays.sort(beanNames);\n\t\t\tfor (String beanName : beanNames) {\n\t\t\t\tSystem.out.println(beanName);\n\t\t\t}\n\n\t\t};\n\t}\n\n}\n'),
#  Document(metadata={'path': 'src/main/java/com/mani/llm/springboot/LLMMainController.java', 'sha': 'e62cbcd41c1ae42794cedf2e6bcc623acfc22cc3', 'source': 'https://api.github.com/maniselvaraj/springboot-demo/blob/main/src/main/java/com/mani/llm/springboot/LLMMainController.java'}, page_content='package com.mani.llm.springboot;\n\nimport org.springframework.web.bind.annotation.GetMapping;\nimport org.springframework.web.bind.annotation.PathVariable;\nimport org.springframework.web.bind.annotation.RestController;\n\n@RestController\npublic class LLMMainController {\n\n\t@GetMapping("/")\n\tpublic String index() {\n\t\treturn "Greetings from Spring Boot Test Project for LLM refactoring!";\n\t}\n\n\n\t@GetMapping("/v1/unique_string/{my_string}")\n\tpublic Boolean checkIfStringHasUniqueCharacters(@PathVariable("my_string") String str ){\n\t\tfor (int i = 0; i < str.length(); i++) {\n\t\t\tfor (int j = 0; j < str.length(); j++) {\n\t\t\t\tif (i != j && str.charAt(i) == str.charAt(j)) {\n\t\t\t\t\treturn false;\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t\treturn true;\n\t}\n\n\n\n\n}\n'), Document(metadata={'path': 'src/test/java/com/mani/llm/springboot/HelloControllerITest.java', 'sha': '6ba7282321c491b41d301d8444f4287a6f9a6763', 'source': 'https://api.github.com/maniselvaraj/springboot-demo/blob/main/src/test/java/com/mani/llm/springboot/HelloControllerITest.java'}, page_content='package com.mani.llm.springboot;\n\nimport org.junit.jupiter.api.Test;\n\nimport org.springframework.beans.factory.annotation.Autowired;\nimport org.springframework.boot.test.context.SpringBootTest;\nimport org.springframework.boot.test.web.client.TestRestTemplate;\nimport org.springframework.http.ResponseEntity;\n\nimport static org.assertj.core.api.Assertions.assertThat;\n\n@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)\npublic class HelloControllerITest {\n\n\t@Autowired\n\tprivate TestRestTemplate template;\n\n    @Test\n    public void getHello() throws Exception {\n        ResponseEntity<String> response = template.getForEntity("/", String.class);\n        assertThat(response.getBody()).isEqualTo("Greetings from Spring Boot!");\n    }\n}\n'), Document(metadata={'path': 'src/test/java/com/mani/llm/springboot/HelloControllerTest.java', 'sha': 'ba753627e92669d1ebbd0953f42a954e5488f244', 'source': 'https://api.github.com/maniselvaraj/springboot-demo/blob/main/src/test/java/com/mani/llm/springboot/HelloControllerTest.java'}, page_content='package com.mani.llm.springboot;\n\nimport static org.hamcrest.Matchers.equalTo;\nimport static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;\nimport static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;\n\nimport org.junit.jupiter.api.Test;\n\nimport org.springframework.beans.factory.annotation.Autowired;\nimport org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;\nimport org.springframework.boot.test.context.SpringBootTest;\nimport org.springframework.http.MediaType;\nimport org.springframework.test.web.servlet.MockMvc;\nimport org.springframework.test.web.servlet.request.MockMvcRequestBuilders;\n\n@SpringBootTest\n@AutoConfigureMockMvc\npublic class HelloControllerTest {\n\n\t@Autowired\n\tprivate MockMvc mvc;\n\n\t@Test\n\tpublic void getHello() throws Exception {\n\t\tmvc.perform(MockMvcRequestBuilders.get("/").accept(MediaType.APPLICATION_JSON))\n\t\t\t\t.andExpect(status().isOk())\n\t\t\t\t.andExpect(content().string(equalTo("Greetings from Spring Boot!")));\n\t}\n}\n')]

def fetch_java_files(file_type="src/main"):
    # print(os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))
    loader = GithubFileLoader(
        repo="maniselvaraj/springboot-demo",  # the repo name
        branch="main",  # the branch name
        access_token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            ".adoc"
        ),  # load all markdowns files.
    )
    documents = loader.load()
    print(documents)
    # Create the data structure while ignoring src/test paths
    java_files_data = [
        {
            'file_source': doc.metadata['source'],  # Java file path
            'page_content': doc.page_content  # Corresponding file content
        }
        for doc in documents
        if doc.metadata['path'].endswith('.java') and doc.metadata['path'].startswith(file_type)
        # Ignore src/test paths
    ]
    return java_files_data


fetch_java_files('/src/main')

