from setuptools import setup

setup(name='gradtest_tools',
        version='1.0.0',
        # packages=['tools'],
        entry_points={
            'console_scripts': [
                'comp_exp = comp_exp:main',
                'eval_acc = eval_acc:main',
                'eval_byte_acc = byte_comp_exp:main',
                'eval_grad = eval_gradient:main',
                'eval_time = eval_runtime:main',
                'eval_dataset = eval_dataset:main',
                'bug_search = bug_search:main',
                'fuzz_gen = generate_fuzzer_info:main',
                'branch_map = branch_map:main'
                ]
            },
        )
