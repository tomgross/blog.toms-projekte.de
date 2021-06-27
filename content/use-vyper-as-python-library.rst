Use vyper as Python library
##############################################
:date: 2021-06-25
:author: Tom
:category: ETH
:tags: Etherum, Vyper, Blockchain
:slug: vyper-as-python-library

One option to program the EVM (Etherum Virtual Machine) is Vyper. As oposed to Solidity,
which borows from JavaScript, Vyper shares its syntax with Python. Installing Vyper
is also done via Python:

.. code-block:: bash

 $ pip install vyper

I wondered if Vyper could be used as library in a Python application, instead of calling
the Vyper compiler via command line. Unfortunately this is not documented in the
Vyper documentation but some source code digging gave me an elegant solution:

.. code-block:: python

    from collections import OrderedDict
    from collections.abc import Iterable
    from vyper.cli import vyper_compile


    def get_vyper_contract(input_files: Iterable[str]) -> OrderedDict:
        output_formats = ["bytecode", "abi"]
        return vyper_compile.compile_files(input_files, output_formats)


    if __name__ == '__main__':
        print(get_vyper_contract(["hello.vy"]))


Assuming we have the following Vyper smart contract as *hello.vy* file ...

.. code-block:: python

    # @version ^0.2.0

    greet: public(String[100])

    @external
    def __init__():
        self.greet = "Hello World"

... we'll get the following result:

.. code-block:: python

    OrderedDict([('hello.vy',
        {'bytecode': '0x600b610140527f48656c6c6f20576f726c640000000000000000000000000000000000000000006101605261014080600060c052602060c020602082510161012060006002818352015b8261012051602002111561005c5761007e565b61012051602002850151610120518501555b8151600101808352811415610049575b50505050505061015756600436101561000d576100c8565b600035601c52600051341561002157600080fd5b63cfae32178114156100c65760008060c052602060c020610180602082540161012060006005818352015b8261012051602002111561005f57610081565b61012051850154610120516020028501525b815160010180835281141561004c575b50505050505061018051806101a001818260206001820306601f82010390500336823750506020610160526040610180510160206001820306601f8201039050610160f35b505b60006000fd5b61008961015703610089600039610089610157036000f3',
         'abi': [{'stateMutability': 'nonpayable', 'type': 'constructor', 'inputs': [], 'outputs': []}, {'stateMutability': 'view', 'type': 'function', 'name': 'greet', 'inputs': [], 'outputs': [{'name': '', 'type': 'string'}], 'gas': 17244}]})
    ])

This technique helps us to create real world applications with web frameworks like Flask
and immutable smart contract storages with Python (and Vyper) only.
