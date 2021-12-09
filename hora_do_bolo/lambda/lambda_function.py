# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# To use handler classes, each request handler is written as a class that implements two methods of 
# the AbstractRequestHandler class; can_handle and handle.
# 
# The can_handle method returns a Boolean value indicating if the request handler can create an 
# appropriate response for the request. The can_handle method has access to the request type and 
# additional attributes that the skill may have set in previous requests or even saved from a 
# previous interaction. The Hello World skill only needs to reference the request information 
# to decide if each handler can respond to an incoming request.


# The LaunchRequest event occurs when the skill is invoked without a specific intent.

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    # The can_handle function returns True if the incoming request is a LaunchRequest
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    # The handle function generates and returns a basic greeting response.
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá! Agora é a Hora do Bolo. Quando é o seu aniversário?"
        reprompt_text = "Eu nasci em 6 de Novembro de 2014. Quando você nasceu?"
        
    # The .ask() function does two things:
    # - Tells the skill to wait for the user to reply, rather than simply exiting
    # - Allows you to specify a way to ask the question to the user again, if they don’t respond
    # A best practice is to make your reprompt text different from your initial speech text.
    # The user may not have responded for a variety of reasons. The skill should pose the initial question 
    # again but do so in a natural way. The reprompt should provide more context to help the user provide 
    # an answer. Specify the reprompt text by creating a new variable named reprompt_text.

        return (
            handler_input.response_builder
                .speak(speak_output) # Calling the .speak() function tells responseBuilder to speak the value of speak_output to the user.
                .ask(speak_output) # Aguarda o usuário para uma nova Intent. Se comentado, finaliza
                .response # This converts the responseBuilder’s work into the response that the skill will return
        )


class CapturaAniversarioIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CapturaAniversarioIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        ano = slots["ano"].value
        mes = slots["mes"].value
        dia = slots["dia"].value

        speak_output = 'Obrigada, eu vou lembrar que você nasceu em {dia} de {mes} de {ano}.'.format(mes=mes, dia=dia, ano=ano)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Você pode dizer olá para mim! Como posso ajudar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Adeus!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, não tenho certeza. Você pode dizer Olá ou Ajuda. O que você gostaria de fazer?"
        reprompt = "Eu não entendi isso. Com o que posso te ajudar"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Você acabou de acionar " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, eu tive problemas em fazer o que você pediu. Por favor, tente novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

# The Lambda handler is the entry point for your AWS Lambda function. The following code example creates 
# a Lambda handler function to route all inbound requests to your skill. The Lambda handler function 
# creates an SDK skill instance configured with the request handlers that you just created

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CapturaAniversarioIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()