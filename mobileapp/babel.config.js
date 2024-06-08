module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          root: ['./'], // adjust this to your source code directory
          alias: {
            app: './app', 
            components: './components', 
            assets: './assets',
          },
        },
      ],
    ],
  };
};
