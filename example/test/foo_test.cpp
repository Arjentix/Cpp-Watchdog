#include <gtest/gtest.h>
#include "foo.h"

TEST(foo, basic) {
    ASSERT_EQ(foo(5), 50);
}
