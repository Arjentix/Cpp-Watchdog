#include <gtest/gtest.h>
#include "bar.h"

TEST(bar, letters) {
    ASSERT_EQ(bar('a'), 'b');
}

TEST(bar, numbers) {
    EXPECT_EQ(bar('0'), '1');
    EXPECT_EQ(bar('1'), '3');
    EXPECT_EQ(bar('8'), '9');
}
