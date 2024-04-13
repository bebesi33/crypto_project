module: {
    rules: [
        {
            test: /\.(jpg|png)$/,
            use: {
              loader: "url-loader",
              options: {
                limit: 25000,
              },
            },
        },
    ],
}
