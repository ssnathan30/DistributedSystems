import os
import subprocess
import pathlib

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
package_dir = pathlib.Path(__file__).parent.parent.resolve()

print(package_dir)


def install_packages():
    # Install gRPC and related packages
    subprocess.run(["pip", "install", "grpcio"], check=True)
    subprocess.run(["pip", "install", "grpcio-tools"], check=True)
    pass


def generate_grpc_code(proto_file):
    # Generate the gRPC code from the proto file
    # The language you want to generate code for (e.g., python)

    try:
        language = 'python'
        # The output directory where the generated code will be stored
        output_dir = package_dir
        # Run the protoc command to generate the code
        subprocess.run(['python3', '-m', 'grpc_tools.protoc', f'-I{output_dir}/proto', f'--pyi_out={output_dir}',
                       f'--{language}_out={output_dir}', f'--grpc_{language}_out={output_dir}', proto_file], check=True)
    except subprocess.CalledProcessError as e:
        print(e.output)


def main():
    install_packages()

    # Your proto file name
    proto_file_customer = "{0}/customer.proto".format(parent_dir)
    proto_file_product = "{0}/product.proto".format(parent_dir)

    generate_grpc_code(proto_file_customer)
    generate_grpc_code(proto_file_product)

if __name__ == "__main__":
    main()
