# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2002(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, message: str=None, buyer_id: int=None):  # noqa: E501
        """InlineResponse2002 - a model defined in Swagger

        :param message: The message of this InlineResponse2002.  # noqa: E501
        :type message: str
        :param buyer_id: The buyer_id of this InlineResponse2002.  # noqa: E501
        :type buyer_id: int
        """
        self.swagger_types = {
            'message': str,
            'buyer_id': int
        }

        self.attribute_map = {
            'message': 'message',
            'buyer_id': 'buyer_id'
        }

        self._message = message
        self._buyer_id = buyer_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2002':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_2 of this InlineResponse2002.  # noqa: E501
        :rtype: InlineResponse2002
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """Gets the message of this InlineResponse2002.


        :return: The message of this InlineResponse2002.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this InlineResponse2002.


        :param message: The message of this InlineResponse2002.
        :type message: str
        """

        self._message = message

    @property
    def buyer_id(self) -> int:
        """Gets the buyer_id of this InlineResponse2002.


        :return: The buyer_id of this InlineResponse2002.
        :rtype: int
        """
        return self._buyer_id

    @buyer_id.setter
    def buyer_id(self, buyer_id: int):
        """Sets the buyer_id of this InlineResponse2002.


        :param buyer_id: The buyer_id of this InlineResponse2002.
        :type buyer_id: int
        """

        self._buyer_id = buyer_id
