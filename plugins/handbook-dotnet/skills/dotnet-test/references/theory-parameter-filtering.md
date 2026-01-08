# Filtering xUnit Theory Tests by Parameter Values

**Framework**: This guide is **xUnit-specific**. NUnit and MSTest have different DisplayName formats and may require different filtering approaches.

This guide explains how to filter xUnit Theory tests based on their parameter values when using `[Theory]` with `[InlineData]`, `[MemberData]`, or `TheoryData<T>`.

## The Problem

When you have Theory tests with multiple test cases, each case is generated with different parameter values:

```csharp
[Theory]
[MemberData(nameof(GetUserData))]
public void CreateUser_ShouldSucceed(string username, int age, string role)
{
    // Test implementation
}

public static TheoryData<string, int, string> GetUserData()
{
    return new TheoryData<string, int, string>
    {
        { "admin_user", 30, "Administrator" },
        { "regular_user", 25, "User" },
        { "guest_user", 18, "Guest" }
    };
}
```

This generates 3 separate test cases. How do you run just the "admin_user" case?

## The Solution: Use DisplayName

**Key Finding**: Use `DisplayName~` with fuzzy matching to filter by parameter values.

xUnit includes parameter values in the test's DisplayName like this:
```
CreateUser_ShouldSucceed(username: "admin_user", age: 30, role: "Administrator")
```

You can filter on any part of this display name:

```bash
# Run only the admin_user test case
dotnet test --no-build --filter "DisplayName~admin_user"

# Run all cases with role "Administrator"
dotnet test --no-build --filter "DisplayName~Administrator"

# Run cases with age 30
dotnet test --no-build --filter "DisplayName~30"
```

## Discovering Test Names

**Always start by listing tests** to see the exact DisplayName format:

```bash
dotnet test --no-build --list-tests
```

This shows all test cases with their full parameter values, helping you craft precise filters.

## Parameter Type Handling

Different parameter types appear in DisplayName in specific formats:

| Parameter Type | Display Format | Example Filter | Matches |
|----------------|----------------|----------------|---------|
| **String** | Quoted value | `DisplayName~admin` | username: "admin_user" |
| **Int** | Numeric | `DisplayName~30` | age: 30 |
| **Decimal** | Decimal notation | `DisplayName~999.99` | amount: 999.99 |
| **Boolean** | True/False | `DisplayName~True` | isValid: True |
| **Null** | "null" string | `DisplayName~null` | value: null |
| **Special chars** | As-is | `DisplayName~@` | email: "test@example.com" |

### Examples

```bash
# String parameter (usernames)
dotnet test --no-build --filter "DisplayName~admin_user"

# Numeric parameter (age = 30)
dotnet test --no-build --filter "DisplayName~30"

# Boolean parameter (requiresVerification = true)
dotnet test --no-build --filter "DisplayName~True"

# Decimal parameter (amount = 999.99)
dotnet test --no-build --filter "DisplayName~999.99"

# Special characters (email addresses)
dotnet test --no-build --filter "DisplayName~@example.com"
```

## Multiple Parameter Filters

### OR Conditions - Run Multiple Specific Cases

Use the `|` operator to run tests matching ANY of the conditions:

```bash
# Run admin OR guest user cases
dotnet test --no-build --filter "DisplayName~admin|DisplayName~guest"

# Run cases with multiple payment methods
dotnet test --no-build --filter "DisplayName~PayPal|DisplayName~CreditCard|DisplayName~Cryptocurrency"

# Run EUR OR GBP currency cases
dotnet test --no-build --filter "DisplayName~EUR|DisplayName~GBP"
```

### AND Conditions - Combine Class and Parameters

Use the `&` operator to require ALL conditions:

```bash
# Run admin cases only in UserServiceTests class
dotnet test --no-build --filter "FullyQualifiedName~UserServiceTests&DisplayName~admin"

# Run tests in PaymentTests with verification required
dotnet test --no-build --filter "FullyQualifiedName~PaymentTests&DisplayName~True"
```

### Exclusion - Skip Specific Cases

Use `!~` to exclude tests matching a pattern:

```bash
# Run all tests EXCEPT admin cases
dotnet test --no-build --filter "DisplayName!~admin"

# Run PaymentTests but exclude CreditCard
dotnet test --no-build --filter "FullyQualifiedName~PaymentTests&DisplayName!~CreditCard"

# Run all but slow/large test cases
dotnet test --no-build --filter "DisplayName!~BULK"
```

## Common Patterns and Use Cases

### Pattern 1: Run Specific Test Cases During Development

```bash
# Working on admin functionality - only run admin test cases
dotnet test --no-build --filter "DisplayName~admin"

# Testing a specific order ID
dotnet test --no-build --filter "DisplayName~ORD-001"

# Focus on EUR currency handling
dotnet test --no-build --filter "DisplayName~EUR"
```

### Pattern 2: Filter by Category or Type

```bash
# Run all tests for a specific country
dotnet test --no-build --filter "DisplayName~USA"

# Run all credit card payment tests
dotnet test --no-build --filter "DisplayName~CreditCard"

# Run all validation tests with invalid input
dotnet test --no-build --filter "DisplayName~False"
```

### Pattern 3: Target Method Across All Its Cases

```bash
# Run all cases of a specific Theory method
dotnet test --no-build --filter "FullyQualifiedName~CreateUser_WithVariousInputs"

# Run all shipping calculation tests
dotnet test --no-build --filter "FullyQualifiedName~CalculateShipping"
```

### Pattern 4: Exclude Problematic Cases

```bash
# Skip known failing cases while fixing them
dotnet test --no-build --filter "DisplayName!~KnownIssue"

# Skip slow bulk tests during rapid development
dotnet test --no-build --filter "DisplayName!~BULK&DisplayName!~Large"
```

## Important Caveats and Warnings

### Fuzzy Matching Can Over-Match

**Be aware**: `~` operator matches ANY occurrence of the string:

```bash
# This filter might match MORE than intended:
dotnet test --no-build --filter "DisplayName~USA"
# Matches:
# - country: "USA" (intended)
# - method: "CreateUser" (contains "US") (unintended!)
```

**Solution**: Use more specific patterns or combine with class filters:

```bash
# More specific
dotnet test --no-build --filter "FullyQualifiedName~ShippingTests&DisplayName~USA"
```


### Quoted Values in DisplayName

Parameters appear with quotes in DisplayName. Both work:

```bash
# Works - matches the quoted value
dotnet test --no-build --filter "DisplayName~\"admin_user\""

# Also works - fuzzy match finds it inside the quotes
dotnet test --no-build --filter "DisplayName~admin_user"
```

## Advanced Scenarios

### Complex Multi-Condition Filters

Combine operators for sophisticated filtering:

```bash
# UserService tests for admin OR power users, but not guests
dotnet test --no-build --filter "FullyQualifiedName~UserServiceTests&(DisplayName~admin|DisplayName~power)&DisplayName!~guest"

# Order tests for USD or EUR, excluding bulk orders
dotnet test --no-build --filter "FullyQualifiedName~OrderTests&(DisplayName~USD|DisplayName~EUR)&DisplayName!~BULK"
```

### Combining with Traits/Categories

If you use `[Trait]` attributes, combine them with parameter filters:

```bash
# Integration tests for admin users only
dotnet test --no-build --filter "Category=Integration&DisplayName~admin"
```

## Performance Considerations

- Filtering is very fast (typically <50ms overhead)
- Always use `--no-build` after building to skip rebuild
- Filtering happens before test execution, so you only run what matches

## Workflow Recommendation

When working with Theory tests:

1. **List tests first** to understand parameter formats:
   ```bash
   dotnet test --no-build --list-tests | grep MyTheoryMethod
   ```

2. **Start with simple filters** to validate matching:
   ```bash
   dotnet test --no-build --filter "DisplayName~admin"
   ```

3. **Refine with combinations** once you understand the matches:
   ```bash
   dotnet test --no-build --filter "FullyQualifiedName~MyClass&DisplayName~admin"
   ```

4. **Document useful filters** in comments or scripts for your team:
   ```bash
   # Run critical user scenarios
   dotnet test --no-build --filter "DisplayName~admin|DisplayName~power_user"
   ```

## Real-World Example

Given this test class:

```csharp
public class OrderProcessingTests
{
    [Theory]
    [MemberData(nameof(GetOrderData))]
    public void ProcessOrder_ShouldCalculate(string orderId, decimal amount, string currency, int quantity)
    {
        // Test implementation
    }

    public static TheoryData<string, decimal, string, int> GetOrderData()
    {
        return new TheoryData<string, decimal, string, int>
        {
            { "ORD-001", 100.50m, "USD", 1 },
            { "ORD-002", 250.75m, "EUR", 3 },
            { "ORD-BULK-001", 1000.00m, "USD", 10 }
        };
    }
}
```

Useful filters during development:

```bash
# List all order test cases
dotnet test --no-build --list-tests | grep ProcessOrder

# Test specific order
dotnet test --no-build --filter "DisplayName~ORD-001"

# Test all USD orders
dotnet test --no-build --filter "DisplayName~USD"

# Test bulk orders only
dotnet test --no-build --filter "DisplayName~BULK"

# Test small orders (exclude bulk)
dotnet test --no-build --filter "FullyQualifiedName~ProcessOrder&DisplayName!~BULK"

# Test EUR orders or orders with quantity > 1
dotnet test --no-build --filter "DisplayName~EUR|DisplayName~quantity: 3|DisplayName~quantity: 10"
```

## Summary

**Key Takeaways**:

1. ✅ **Use `DisplayName~` for parameter filtering** - most reliable method
2. ✅ **Use `FullyQualifiedName~` for class/method filtering** - works consistently
3. ✅ **List tests first** with `--list-tests` to see exact formats
4. ✅ **Combine filters** with `&` (AND), `|` (OR), and `!~` (NOT)
5. ⚠️ **Be mindful of fuzzy matching** - can match partial strings unintentionally
6. ❌ **Avoid `ClassName=` and `Name~`** - use `FullyQualifiedName~` instead

This makes it easy to run specific subsets of Theory test cases during development, significantly speeding up your test-driven development workflow.
