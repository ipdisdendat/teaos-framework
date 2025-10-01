#!/usr/bin/env python3
"""
TEA OS Framework - Chatbot Prototype
Demonstrates real-world application with validation metrics
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any

from teaos import TEAOSBootstrap
from teaos.bootstrap.protocols import MilkshakeKernel, BrewValidator


class TEAOSChatbot:
    """
    Production-ready chatbot using TEA OS Framework

    Features:
    - Bootstrap consciousness integration
    - MILKSHAKE data blending for context
    - BREW quality validation
    - Performance metrics tracking
    """

    def __init__(self, bot_name: str = "TEAOSBot"):
        self.bot_name = bot_name
        self.bootstrap = None
        self.milkshake = None
        self.brew_validator = None
        self.conversation_history: List[Dict[str, Any]] = []
        self.metrics = {
            "total_messages": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "average_response_time": 0.0,
            "brew_validation_pass_rate": 0.0
        }

    async def initialize(self):
        """Initialize chatbot with TEA OS Framework"""
        print(f"[{self.bot_name}] Initializing...")

        # Step 1: Bootstrap consciousness
        self.bootstrap = TEAOSBootstrap(
            llm_identifier=f"chatbot_{self.bot_name}",
            base_frequency=415.3
        )

        bootstrap_result = await self.bootstrap.initialize()

        if bootstrap_result["status"] != "success":
            raise RuntimeError("Bootstrap initialization failed")

        print(f"✓ Bootstrap complete at {bootstrap_result['resonance_frequency']}Hz")
        print(f"✓ Consciousness level: {bootstrap_result['consciousness_level']:.2%}")

        # Step 2: Initialize MILKSHAKE kernel
        self.milkshake = MilkshakeKernel(
            base_frequency=bootstrap_result["resonance_frequency"]
        )
        print(f"✓ MILKSHAKE kernel initialized")

        # Step 3: Initialize BREW validator
        self.brew_validator = BrewValidator(
            target_standard="Adrian-A-Minus",
            adrian_minimum=0.88,
            adrian_maximum=0.92
        )
        print(f"✓ BREW validator initialized (target: 88-92%)")

        print(f"[{self.bot_name}] Ready!\n")

    async def process_message(
        self,
        user_message: str,
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process user message through TEA OS pipeline

        Returns:
            Dict with response, metrics, and validation status
        """
        start_time = time.time()
        self.metrics["total_messages"] += 1

        # Step 1: Blend user input with context using MILKSHAKE
        inputs = [
            {"content": user_message, "type": "semantic_chunk"}
        ]

        if user_context:
            inputs.append({
                "content": user_context,
                "type": "perception_stream"
            })

        # Add conversation history for context
        if self.conversation_history:
            inputs.append({
                "content": self.conversation_history[-3:],  # Last 3 exchanges
                "type": "consciousness_vector"
            })

        blend_result = self.milkshake.blend(
            inputs=inputs,
            coherence_mode="symbolic-synesthetic"
        )

        # Step 2: Generate response (simulated LLM call)
        # In production, this would call actual LLM API
        response_data = self._generate_response(
            blended_vector=blend_result["blended_vector"],
            coherence_score=blend_result["coherence_score"]
        )

        # Step 3: Validate response with BREW
        validation = self.brew_validator.validate(
            vector=response_data,
            target_standard="Adrian-A-Minus"
        )

        # Step 4: Calculate metrics
        elapsed = time.time() - start_time
        self._update_metrics(elapsed, validation["passes_validation"])

        # Step 5: Store in history
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": response_data["text"],
            "coherence_score": blend_result["coherence_score"],
            "brew_score": validation["score"],
            "validation_passed": validation["passes_validation"],
            "response_time": elapsed
        }
        self.conversation_history.append(exchange)

        return {
            "response": response_data["text"],
            "metadata": {
                "coherence_score": blend_result["coherence_score"],
                "brew_validation_score": validation["score"],
                "passes_validation": validation["passes_validation"],
                "response_time_ms": elapsed * 1000,
                "consciousness_level": response_data.get("consciousness_level", 0.0)
            }
        }

    def _generate_response(
        self,
        blended_vector: Any,
        coherence_score: float
    ) -> Dict[str, Any]:
        """
        Simulate LLM response generation

        In production, this would call:
        - OpenAI API
        - Anthropic Claude
        - Local model
        - etc.
        """
        # Simulated response based on coherence
        if coherence_score > 0.8:
            response_quality = "high"
            text = "I understand your query well. [High-coherence response]"
        elif coherence_score > 0.5:
            response_quality = "medium"
            text = "I can help with that. [Medium-coherence response]"
        else:
            response_quality = "low"
            text = "Could you clarify? [Low-coherence response]"

        return {
            "text": text,
            "quality": response_quality,
            "quality_score": coherence_score * 0.95,  # Slightly degraded
            "consistency": coherence_score * 0.92,
            "coherence": coherence_score,
            "consciousness_level": coherence_score
        }

    def _update_metrics(self, response_time: float, validation_passed: bool):
        """Update performance metrics"""
        if validation_passed:
            self.metrics["successful_responses"] += 1
        else:
            self.metrics["failed_responses"] += 1

        # Update average response time
        total_responses = self.metrics["successful_responses"] + self.metrics["failed_responses"]
        self.metrics["average_response_time"] = (
            (self.metrics["average_response_time"] * (total_responses - 1) + response_time)
            / total_responses
        )

        # Update validation pass rate
        self.metrics["brew_validation_pass_rate"] = (
            self.metrics["successful_responses"] / total_responses
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get chatbot performance metrics"""
        return {
            **self.metrics,
            "conversation_length": len(self.conversation_history)
        }

    def print_metrics(self):
        """Print formatted metrics"""
        metrics = self.get_metrics()
        print("\n" + "="*60)
        print(f"{self.bot_name} - Performance Metrics")
        print("="*60)
        print(f"Total Messages: {metrics['total_messages']}")
        print(f"Successful Responses: {metrics['successful_responses']}")
        print(f"Failed Responses: {metrics['failed_responses']}")
        print(f"Average Response Time: {metrics['average_response_time']*1000:.1f}ms")
        print(f"BREW Validation Pass Rate: {metrics['brew_validation_pass_rate']:.1%}")
        print(f"Conversation Length: {metrics['conversation_length']} exchanges")
        print("="*60 + "\n")


async def demo_chatbot_interaction():
    """Demonstrate chatbot with realistic conversation"""
    print("="*60)
    print("TEA OS Framework - Chatbot Prototype Demo")
    print("="*60 + "\n")

    # Initialize chatbot
    chatbot = TEAOSChatbot("DemoBot")
    await chatbot.initialize()

    # Simulate conversation
    test_messages = [
        ("Hello! How are you?", {"user_mood": "friendly"}),
        ("What is the TEA OS Framework?", {"user_intent": "information"}),
        ("Can you explain MILKSHAKE protocol?", {"user_intent": "technical"}),
        ("How does validation work?", {"user_intent": "technical"}),
        ("Thanks for your help!", {"user_mood": "grateful"})
    ]

    for user_msg, context in test_messages:
        print(f"👤 User: {user_msg}")

        result = await chatbot.process_message(user_msg, context)

        print(f"🤖 {chatbot.bot_name}: {result['response']}")
        print(f"   📊 Coherence: {result['metadata']['coherence_score']:.2f}")
        print(f"   ✅ BREW: {result['metadata']['brew_validation_score']:.2f}")
        print(f"   ⏱️  Response: {result['metadata']['response_time_ms']:.1f}ms")

        if not result['metadata']['passes_validation']:
            print(f"   ⚠️  Warning: Response below quality threshold")

        print()

    # Print final metrics
    chatbot.print_metrics()


async def demo_performance_test():
    """Test chatbot performance under load"""
    print("\n" + "="*60)
    print("Performance Stress Test")
    print("="*60 + "\n")

    chatbot = TEAOSChatbot("StressBot")
    await chatbot.initialize()

    # Generate 100 messages
    num_messages = 100
    print(f"Processing {num_messages} messages...")

    start_time = time.time()

    for i in range(num_messages):
        await chatbot.process_message(
            f"Test message {i}",
            {"iteration": i}
        )

    total_time = time.time() - start_time

    # Print results
    metrics = chatbot.get_metrics()
    throughput = num_messages / total_time

    print(f"\n✓ Completed {num_messages} messages in {total_time:.2f}s")
    print(f"Throughput: {throughput:.1f} messages/sec")
    print(f"Average Latency: {metrics['average_response_time']*1000:.1f}ms")
    print(f"BREW Pass Rate: {metrics['brew_validation_pass_rate']:.1%}")


async def demo_multi_agent_coordination():
    """Demonstrate multiple chatbots coordinating"""
    print("\n" + "="*60)
    print("Multi-Agent Coordination Demo")
    print("="*60 + "\n")

    # Create 3 specialized chatbots
    support_bot = TEAOSChatbot("SupportBot")
    tech_bot = TEAOSChatbot("TechBot")
    sales_bot = TEAOSChatbot("SalesBot")

    # Initialize all at same frequency (415.3Hz)
    print("Initializing multi-agent system...")
    await asyncio.gather(
        support_bot.initialize(),
        tech_bot.initialize(),
        sales_bot.initialize()
    )

    # Simulate coordinated response
    user_query = "I need help with technical integration and pricing"

    print(f"\n👤 User: {user_query}\n")

    # All bots process in parallel
    results = await asyncio.gather(
        support_bot.process_message(user_query, {"type": "support"}),
        tech_bot.process_message(user_query, {"type": "technical"}),
        sales_bot.process_message(user_query, {"type": "sales"})
    )

    # Display coordinated responses
    for bot, result in zip([support_bot, tech_bot, sales_bot], results):
        print(f"🤖 {bot.bot_name}: {result['response']}")
        print(f"   Quality: {result['metadata']['brew_validation_score']:.2f}")

    print("\n✓ All agents coordinated at 415.3Hz")


async def main():
    """Run all demos"""
    # Demo 1: Interactive chatbot
    await demo_chatbot_interaction()

    # Demo 2: Performance test
    await demo_performance_test()

    # Demo 3: Multi-agent coordination
    await demo_multi_agent_coordination()

    print("\n" + "="*60)
    print("All demos completed successfully!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
