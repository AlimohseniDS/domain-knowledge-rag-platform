# Primary Local Model

## Selected checkpoint

```text
Qwen/Qwen3.5-35B-A3B-GPTQ-Int4
```

This is the official Qwen GPTQ 4-bit post-trained checkpoint. The initial deployment target is one NVIDIA RTX A6000 with 48 GB VRAM.

## Why this profile is conservative

Although the model supports a much larger native context, the initial RAG service limits the operational context to 32K. This leaves capacity for the KV cache and concurrent requests. RAG should retrieve a small set of strong passages rather than place entire documents into the prompt.

The first profile is text-only. Skipping the vision encoder frees additional GPU memory. Multimodal ingestion can be enabled later as a separately measured feature.

## Server environment

Use an isolated Python environment on the Linux GPU server. Qwen3.5 currently requires a sufficiently recent vLLM build; follow the official checkpoint instructions when pinning the production version.

Example installation:

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install vllm --torch-backend=auto \
  --extra-index-url https://wheels.vllm.ai/nightly
```

Do not leave production dependencies unpinned after validation. Record the working vLLM, PyTorch, CUDA driver, and NVIDIA driver versions in the deployment manifest.

## Initial serving command

```bash
vllm serve Qwen/Qwen3.5-35B-A3B-GPTQ-Int4 \
  --host 0.0.0.0 \
  --port 8000 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --reasoning-parser qwen3 \
  --language-model-only \
  --quantization moe_wna16
```

Tensor parallelism is intentionally omitted because this profile targets one GPU.

## API configuration

The server exposes an OpenAI-compatible API:

```env
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://llm:8000/v1
LLM_API_KEY=local-vllm
LLM_MODEL=Qwen/Qwen3.5-35B-A3B-GPTQ-Int4
```

The local API key is a compatibility value unless authentication is explicitly enabled at the model server or reverse proxy.

## Smoke test

```bash
curl http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen/Qwen3.5-35B-A3B-GPTQ-Int4",
    "messages": [
      {
        "role": "user",
        "content": "Reply with exactly: local model ready"
      }
    ],
    "temperature": 0,
    "max_tokens": 20
  }'
```

## Deployment validation

Before accepting the model profile:

1. Confirm that the server starts without CPU offloading.
2. Record idle and peak GPU memory with `nvidia-smi`.
3. Measure time to first token and generation throughput at 2K, 8K, 16K, and 32K prompts.
4. Test one, two, and four concurrent requests.
5. Run the versioned domain RAG evaluation set.
6. Verify citation fidelity and insufficient-evidence behavior.
7. Reduce `VLLM_MAX_MODEL_LEN` or concurrency if the server approaches out-of-memory conditions.

## Production note

The model weights should be downloaded during an explicit provisioning step and cached in persistent local storage. After provisioning, local inference must not require internet access.
