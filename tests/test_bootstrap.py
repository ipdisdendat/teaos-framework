#!/usr/bin/env python3
"""
TEA OS Framework - Bootstrap Validation Tests
Comprehensive test suite for bootstrap functionality
"""

import pytest
import asyncio
import time
from typing import Dict, Any

# Import from the framework
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from teaos import TEAOSBootstrap
from teaos.bootstrap.protocols import MilkshakeKernel, BrewValidator


class TestBootstrapCore:
    """Test core bootstrap functionality"""

    def test_bootstrap_initialization(self):
        """Test basic bootstrap initialization"""
        bootstrap = TEAOSBootstrap(
            llm_identifier="test_llm",
            base_frequency=415.3
        )

        assert bootstrap.llm_id == "test_llm"
        assert bootstrap.base_frequency == 415.3
        assert bootstrap.target_standard == "Adrian-A-Minus"

    def test_bootstrap_with_custom_frequency(self):
        """Test bootstrap with custom frequency"""
        custom_freq = 420.0
        bootstrap = TEAOSBootstrap(
            llm_identifier="custom_llm",
            base_frequency=custom_freq
        )

        assert bootstrap.base_frequency == custom_freq

    @pytest.mark.asyncio
    async def test_bootstrap_initialize_success(self):
        """Test successful bootstrap initialization"""
        bootstrap = TEAOSBootstrap("test_init")
        result = await bootstrap.initialize()

        # Verify result structure
        assert "status" in result
        assert result["status"] == "success"
        assert "bootstrap_id" in result
        assert "resonance_frequency" in result
        assert "harmonic_signature" in result
        assert "field_connection" in result
        assert "consciousness_level" in result
        assert "brew_validation_score" in result
        assert "tea_os_coordinates" in result

    @pytest.mark.asyncio
    async def test_bootstrap_consciousness_coordinates(self):
        """Test consciousness coordinates generation"""
        bootstrap = TEAOSBootstrap("test_coords")
        result = await bootstrap.initialize()

        coords = result["tea_os_coordinates"]

        # Verify mathematical constants
        assert "phi" in coords
        assert abs(coords["phi"] - 1.618033988749895) < 0.0001
        assert "pi" in coords
        assert abs(coords["pi"] - 3.141592653589793) < 0.0001
        assert "e" in coords
        assert abs(coords["e"] - 2.718281828459045) < 0.0001
        assert coords["frequency"] == 415.3
        assert coords["sacred_epsilon"] == 0.03


class TestMilkshakeProtocol:
    """Test MILKSHAKE Protocol functionality"""

    def test_milkshake_kernel_initialization(self):
        """Test MilkshakeKernel initialization"""
        kernel = MilkshakeKernel(base_frequency=415.3)

        assert kernel.base_frequency == 415.3

    def test_milkshake_blend_basic(self):
        """Test basic MILKSHAKE blending"""
        kernel = MilkshakeKernel()

        inputs = [
            {"content": "test_data", "type": "semantic_chunk"}
        ]

        result = kernel.blend(
            inputs=inputs,
            coherence_mode="symbolic-synesthetic"
        )

        assert "coherence_score" in result
        assert 0.0 <= result["coherence_score"] <= 1.0
        assert "blended_vector" in result

    def test_milkshake_multiple_inputs(self):
        """Test MILKSHAKE with multiple input sources"""
        kernel = MilkshakeKernel()

        inputs = [
            {"content": "input_1", "type": "semantic_chunk"},
            {"content": "input_2", "type": "perception_stream"},
            {"content": "input_3", "type": "consciousness_vector"}
        ]

        result = kernel.blend(
            inputs=inputs,
            coherence_mode="symbolic-synesthetic"
        )

        assert result["coherence_score"] >= 0.0


class TestBrewValidation:
    """Test BREW Validation functionality"""

    def test_brew_validator_initialization(self):
        """Test BrewValidator initialization"""
        validator = BrewValidator(
            target_standard="Adrian-A-Minus",
            adrian_minimum=0.88,
            adrian_maximum=0.92
        )

        assert validator.target_standard == "Adrian-A-Minus"
        assert validator.adrian_minimum == 0.88
        assert validator.adrian_maximum == 0.92

    def test_brew_validation_pass(self):
        """Test BREW validation with passing score"""
        validator = BrewValidator()

        # Create test vector with high quality
        test_vector = {
            "quality_score": 0.90,
            "consistency": 0.89,
            "coherence": 0.91
        }

        result = validator.validate(
            vector=test_vector,
            target_standard="Adrian-A-Minus"
        )

        assert "passes_validation" in result
        assert "score" in result
        assert "validation_stages" in result

    def test_brew_validation_fail(self):
        """Test BREW validation with failing score"""
        validator = BrewValidator()

        # Create test vector with low quality
        test_vector = {
            "quality_score": 0.50,
            "consistency": 0.45,
            "coherence": 0.48
        }

        result = validator.validate(
            vector=test_vector,
            target_standard="Adrian-A-Minus"
        )

        # Should fail or provide degraded score
        assert "score" in result
        assert result["score"] < 0.88  # Below Adrian-A-Minus minimum


class TestPerformanceMetrics:
    """Test performance characteristics"""

    @pytest.mark.asyncio
    async def test_bootstrap_initialization_speed(self):
        """Test bootstrap initialization performance"""
        bootstrap = TEAOSBootstrap("perf_test")

        start_time = time.time()
        result = await bootstrap.initialize()
        elapsed = time.time() - start_time

        # Should complete within reasonable time (< 1 second)
        assert elapsed < 1.0
        assert result["status"] == "success"
        print(f"\nBootstrap initialization: {elapsed:.3f}s")

    def test_milkshake_blend_speed(self):
        """Test MILKSHAKE blending performance"""
        kernel = MilkshakeKernel()

        inputs = [{"content": f"input_{i}", "type": "semantic_chunk"}
                  for i in range(10)]

        start_time = time.time()
        result = kernel.blend(inputs=inputs, coherence_mode="symbolic-synesthetic")
        elapsed = time.time() - start_time

        # Should be fast (< 100ms for 10 inputs)
        assert elapsed < 0.1
        print(f"\nMILKSHAKE blend (10 inputs): {elapsed*1000:.1f}ms")

    @pytest.mark.asyncio
    async def test_concurrent_bootstrap(self):
        """Test multiple concurrent bootstrap operations"""
        async def bootstrap_task(llm_id):
            bootstrap = TEAOSBootstrap(llm_id)
            return await bootstrap.initialize()

        start_time = time.time()

        # Run 5 bootstraps concurrently
        tasks = [bootstrap_task(f"concurrent_{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)

        elapsed = time.time() - start_time

        # All should succeed
        assert all(r["status"] == "success" for r in results)
        # Should benefit from concurrency (< 2x single bootstrap time)
        assert elapsed < 2.0
        print(f"\n5 concurrent bootstraps: {elapsed:.3f}s")


class TestIntegrationScenarios:
    """Test real-world integration scenarios"""

    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """Test complete pipeline: Bootstrap → MILKSHAKE → BREW"""
        # Step 1: Bootstrap
        bootstrap = TEAOSBootstrap("pipeline_test")
        bootstrap_result = await bootstrap.initialize()
        assert bootstrap_result["status"] == "success"

        # Step 2: MILKSHAKE blend
        kernel = MilkshakeKernel(
            base_frequency=bootstrap_result["resonance_frequency"]
        )
        inputs = [
            {"content": "user query", "type": "semantic_chunk"},
            {"content": "context data", "type": "perception_stream"}
        ]
        blend_result = kernel.blend(
            inputs=inputs,
            coherence_mode="symbolic-synesthetic"
        )
        assert blend_result["coherence_score"] > 0.0

        # Step 3: BREW validation
        validator = BrewValidator()
        validation_result = validator.validate(
            vector=blend_result["blended_vector"],
            target_standard="Adrian-A-Minus"
        )
        assert "score" in validation_result

        print(f"\nPipeline test:")
        print(f"  Bootstrap: {bootstrap_result['status']}")
        print(f"  MILKSHAKE coherence: {blend_result['coherence_score']:.2f}")
        print(f"  BREW validation: {validation_result['score']:.2f}")

    @pytest.mark.asyncio
    async def test_multi_agent_coordination(self):
        """Test multiple agents with shared frequency"""
        # Create 3 agents at same frequency
        agent_a = TEAOSBootstrap("agent_a", base_frequency=415.3)
        agent_b = TEAOSBootstrap("agent_b", base_frequency=415.3)
        agent_c = TEAOSBootstrap("agent_c", base_frequency=415.3)

        # Initialize all
        results = await asyncio.gather(
            agent_a.initialize(),
            agent_b.initialize(),
            agent_c.initialize()
        )

        # All should succeed and have same frequency
        assert all(r["status"] == "success" for r in results)
        assert all(r["resonance_frequency"] == 415.3 for r in results)

        # Verify unique identities despite same frequency
        ids = [r["bootstrap_id"] for r in results]
        assert len(set(ids)) == 3  # All unique

        print(f"\nMulti-agent coordination:")
        for i, result in enumerate(results):
            print(f"  Agent {chr(65+i)}: {result['bootstrap_id']}")


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_frequency(self):
        """Test bootstrap with invalid frequency"""
        with pytest.raises((ValueError, TypeError)):
            bootstrap = TEAOSBootstrap("test", base_frequency="invalid")

    def test_invalid_target_standard(self):
        """Test bootstrap with invalid standard"""
        bootstrap = TEAOSBootstrap(
            "test",
            target_standard="Invalid-Standard"
        )
        # Should handle gracefully
        assert bootstrap.target_standard == "Invalid-Standard"

    def test_empty_milkshake_inputs(self):
        """Test MILKSHAKE with empty inputs"""
        kernel = MilkshakeKernel()

        result = kernel.blend(
            inputs=[],
            coherence_mode="symbolic-synesthetic"
        )

        # Should handle gracefully with zero score
        assert result["coherence_score"] == 0.0


# Benchmark Suite
class TestBenchmarks:
    """Performance benchmarks for comparison"""

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_benchmark_bootstrap_throughput(self):
        """Benchmark bootstrap throughput"""
        iterations = 100

        start_time = time.time()
        for i in range(iterations):
            bootstrap = TEAOSBootstrap(f"bench_{i}")
            await bootstrap.initialize()
        elapsed = time.time() - start_time

        throughput = iterations / elapsed
        print(f"\nBootstrap throughput: {throughput:.1f} ops/sec")
        print(f"Average latency: {elapsed/iterations*1000:.1f}ms")

        # Should achieve reasonable throughput
        assert throughput > 10  # At least 10 bootstraps/sec

    @pytest.mark.benchmark
    def test_benchmark_milkshake_throughput(self):
        """Benchmark MILKSHAKE throughput"""
        kernel = MilkshakeKernel()
        inputs = [{"content": f"input_{i}", "type": "semantic_chunk"}
                  for i in range(5)]

        iterations = 1000

        start_time = time.time()
        for _ in range(iterations):
            kernel.blend(inputs=inputs, coherence_mode="symbolic-synesthetic")
        elapsed = time.time() - start_time

        throughput = iterations / elapsed
        print(f"\nMILKSHAKE throughput: {throughput:.1f} ops/sec")
        print(f"Average latency: {elapsed/iterations*1000:.2f}ms")

        # Should be very fast
        assert throughput > 100  # At least 100 blends/sec


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
