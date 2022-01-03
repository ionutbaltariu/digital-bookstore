package com.example.pos.stateless.endpoints

import org.springframework.boot.web.servlet.ServletRegistrationBean
import org.springframework.context.ApplicationContext
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.io.ClassPathResource
import org.springframework.ws.config.annotation.EnableWs
import org.springframework.ws.config.annotation.WsConfigurerAdapter
import org.springframework.ws.transport.http.MessageDispatcherServlet
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition
import org.springframework.xml.xsd.SimpleXsdSchema
import org.springframework.xml.xsd.XsdSchema

@EnableWs
@Configuration
class WebServiceConfig : WsConfigurerAdapter() {
    @Bean
    fun messageDispatcherServlet(applicationContext: ApplicationContext?): ServletRegistrationBean<*> {
        val result = MessageDispatcherServlet()
        result.setApplicationContext(applicationContext!!)
        result.isTransformWsdlLocations = true
        return ServletRegistrationBean(result, "/sample/*")
    }

    @Bean(name = ["Calculator"])
    fun defaultWsdl11Definition(calculatorSchema: XsdSchema?): DefaultWsdl11Definition {
        val result = DefaultWsdl11Definition()
        result.setPortTypeName("CalculatorPort")
        result.setLocationUri("/sample")
        result.setTargetNamespace("http://pos.examples.soap.stateless/Calculator")
        result.setSchema(calculatorSchema)
        return result
    }

    @Bean
    fun calculatorSchema(): XsdSchema {
        return SimpleXsdSchema(ClassPathResource("Calculator.xsd"))
    }
}