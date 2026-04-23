from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="echarts-for-ai",
    version="2.0.0",
    author="Skill工厂·牧云野店",
    author_email="support@echarts-for-ai.com",
    description="专业的AI Agent数据可视化库 - 商业化就绪，企业级质量",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenshuai9101/echarts-viz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "full": [
            "pyecharts>=1.9.0",
            "playwright>=1.30.0",
        ],
    },
    include_package_data=True,
    package_data={
        "echarts_for_ai": ["templates/*.html", "themes/*.json"],
    },
    entry_points={
        "console_scripts": [
            "echarts-ai=echarts_for_ai.cli:main",
        ],
    },
)
