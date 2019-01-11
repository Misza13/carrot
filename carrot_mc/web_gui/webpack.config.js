const path = require('path');

module.exports = {
    mode: "production",
    entry: "./src/main.jsx",
    devtool: "sourcemap",
    output : {
        path: path.resolve(__dirname, "static")
    },
    module: {
        rules: [
            {
                test: /\.jsx$/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "main.css"
                        }
                    },
                    "extract-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.scss/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "main.css"
                        },
                    },
                    "extract-loader",
                    "scss-loader"
                ]
            },
            {
                test: /\.(woff2?|svg)$/,
                loader: 'url-loader?limit=10000'
            },
            {
                test: /\.(ttf|eot)$/,
                loader: 'file-loader'
            },
        ]
    }
};