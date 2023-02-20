# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from seller_server.models.base_model_ import Model
from seller_server import util


class InlineResponse201(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, message: str=None):  # noqa: E501
        """InlineResponse201 - a model defined in Swagger

        :param message: The message of this InlineResponse201.  # noqa: E501
        :type message: str
        """
        self.swagger_types = {
            'message': str
        }

        self.attribute_map = {
            'message': 'message'
        }

        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse201':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_201 of this InlineResponse201.  # noqa: E501
        :rtype: InlineResponse201
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """Gets the message of this InlineResponse201.

        Success message  # noqa: E501

        :return: The message of this InlineResponse201.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this InlineResponse201.

        Success message  # noqa: E501

        :param message: The message of this InlineResponse201.
        :type message: str
        """

        self._message = message
