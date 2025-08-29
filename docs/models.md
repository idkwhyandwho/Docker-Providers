# Model Configuration Guide

## Supported Model Formats

The Docker Model Runner supports various model formats:

1. ONNX
2. PyTorch (TorchScript)
3. TensorFlow SavedModel
4. Custom formats (with appropriate runners)

## Model Setup

1. Place model files in the `models` directory
2. Update `config/config.json` with model details:
   ```json
   {
       "models": {
           "model-name": {
               "image": "model-runner-image",
               "model_path": "/models/path",
               "parameters": {}
           }
       }
   }
   ```

## Model Runner Images

Available runner images:

1. `ai/model-runner:latest`
   - General purpose model runner
   - Supports multiple formats
   - GPU acceleration

2. `ai/embedding-runner:latest`
   - Specialized for embeddings
   - Optimized for throughput

## Custom Model Runners

To create a custom runner:

1. Create a Dockerfile:
   ```dockerfile
   FROM ai/model-runner-base:latest
   
   # Add custom dependencies
   RUN pip install custom-deps
   
   # Add custom code
   COPY custom_runner.py /app/
   ```

2. Implement the runner interface
3. Build and tag the image
4. Update configuration to use the custom runner

## Performance Tuning

Model performance can be optimized through:

1. Batch size configuration
2. Quantization settings
3. Cache settings
4. GPU memory optimization

See `docs/performance.md` for details.
